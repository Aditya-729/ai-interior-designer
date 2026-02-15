"""
Inference endpoints for image editing.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.image import Image
from app.db.models.version import Version
from app.db.models.history import EditHistory
from app.services.inference_client import inference_client
from app.services.storage import storage
from app.services.websocket_manager import websocket_manager
from app.services.gpu_queue import gpu_queue
from app.services.usage_limiter import UsageLimiter
from app.middleware.auth import require_auth
from typing import Optional, Dict, Any
import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/run-inpainting")
async def run_inpainting(
    image_id: str = Body(...),
    edit_plan: Dict[str, Any] = Body(...),
    project_id: Optional[str] = Body(None),
    client_id: Optional[str] = Body(None),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Execute image editing based on edit plan.

    Forwards request to inference_service and streams progress via websocket.
    Saves generated version.

    Returns:
        {
            "version_id": "...",
            "image_url": "...",
            "processing_time": 45.2
        }
    """
    # Require authentication
    user_id = await require_auth(request)
    
    # Check usage limits
    limiter = UsageLimiter(db)
    allowed, message = limiter.check_inference_limit(user_id)
    if not allowed:
        raise HTTPException(status_code=403, detail=message)
    
    # Check ownership of image/project
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    if project_id:
        from app.db.models.project import Project
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    start_time = time.time()
    
    # Generate job ID
    import uuid
    job_id = str(uuid.uuid4())
    
    # Check GPU queue
    queue_status = gpu_queue.get_queue_status()
    if queue_status["queued"] >= 10:
        raise HTTPException(status_code=503, detail="GPU queue is full. Please try again later.")
    
    # Send queue status to client
    if client_id:
        await websocket_manager.send_message(
            client_id,
            {
                "status": "queued",
                "queue_position": queue_status["queued"] + 1,
                "message": f"Queued for processing (position {queue_status['queued'] + 1})",
            }
        )

    try:

        # Send progress update
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 10, "message": "Starting edit..."}
            )

        # Download source image
        import httpx
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(db_image.original_url)
            response.raise_for_status()
            image_data = response.content

        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 30, "message": "Preparing inference..."}
            )

        # Define inference execution function
        async def execute_inference(job_data: dict):
            nonlocal result_image
            edits = edit_plan.get("edits", [])
            room_type = edit_plan.get("room_type", "room")

            if client_id:
                await websocket_manager.send_message(
                    client_id,
                    {"status": "processing", "progress": 50, "message": "Running AI model..."}
                )

            # Call inference service
            result_image = await inference_client.run_multi_edit(
                image_data=job_data["image_data"],
                edits=edits,
                room_type=room_type,
            )

        # Submit to GPU queue
        await gpu_queue.submit_job(
            job_id=job_id,
            job_data={"image_data": image_data},
            execute_fn=execute_inference,
        )
        
        # Wait for job to complete (simplified - in production use proper async waiting)
        # For now, we'll process synchronously but with queue management
        edits = edit_plan.get("edits", [])
        room_type = edit_plan.get("room_type", "room")

        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 50, "message": "Running AI model..."}
            )

        # Call inference service
        result_image = await inference_client.run_multi_edit(
            image_data=image_data,
            edits=edits,
            room_type=room_type,
        )
        
        # Increment usage
        limiter.increment_inference_count(user_id)

        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 90, "message": "Saving result..."}
            )

        # Upload result
        storage_key = storage.generate_key("versions", "edited.jpg")
        result_url = storage.upload_file(
            result_image, storage_key, content_type="image/jpeg"
        )

        processing_time = time.time() - start_time

        # Save version
        version = Version(
            project_id=project_id or db_image.project_id,
            image_url=result_url,
            storage_key=storage_key,
            edit_plan=edit_plan,
            user_prompt=edit_plan.get("original_prompt"),
        )
        db.add(version)
        db.commit()
        db.refresh(version)

        # Save edit history
        history = EditHistory(
            project_id=project_id or db_image.project_id,
            version_id=version.id,
            user_prompt=edit_plan.get("original_prompt"),
            edit_plan=edit_plan,
            processing_time=processing_time,
        )
        db.add(history)
        db.commit()

        if client_id:
            await websocket_manager.send_message(
                client_id,
                {
                    "status": "completed",
                    "progress": 100,
                    "message": "Edit complete!",
                    "version_id": version.id,
                    "image_url": result_url,
                }
            )

        logger.info(f"Inference complete: {version.id}, time={processing_time:.2f}s")
        
        # Increment edit count
        limiter.increment_edit_count(user_id)

        return {
            "version_id": version.id,
            "image_url": result_url,
            "processing_time": processing_time,
            "queue_status": gpu_queue.get_queue_status(),
        }

    except Exception as e:
        logger.error(f"Inference failed: {e}")
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "error", "message": f"Edit failed: {str(e)}"}
            )
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
