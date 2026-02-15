"""
Inference endpoints for image editing.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.inference_client import inference_client
from app.storage import storage
from app.models import Image, Version, EditHistory, Project
from app.websocket import websocket_manager
from typing import Dict, Any, Optional
import httpx
import time

router = APIRouter()


@router.post("/run-inpainting")
async def run_inpainting(
    image_id: str = Body(...),
    edit_plan: Dict[str, Any] = Body(...),
    project_id: Optional[str] = Body(None),
    client_id: Optional[str] = Body(None),
    db: Session = Depends(get_db),
):
    """
    Execute image editing based on edit plan.

    Args:
        image_id: Source image ID
        edit_plan: Structured edit plan from planner
        project_id: Optional project ID
        client_id: WebSocket client ID for progress updates

    Returns:
        {
            "version_id": "...",
            "image_url": "...",
            "processing_time": 45.2
        }
    """
    start_time = time.time()

    # Get source image
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Download source image
    async with httpx.AsyncClient() as client:
        response = await client.get(db_image.original_url)
        response.raise_for_status()
        image_data = response.content

    # Send progress update
    if client_id:
        await websocket_manager.send_message(
            client_id, {"status": "processing", "progress": 10, "message": "Starting edit..."}
        )

    # Get masks for edits (this should be integrated with Mino results)
    # For now, we'll need to fetch masks from the edit plan or Mino service
    # This is a simplified version - in production, masks should be stored/retrieved properly

    # Run inference
    try:
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 50, "message": "Running AI model..."},
            )

        # For multi-edit, use run_multi_edit
        # For single edit, use run_inpainting
        edits = edit_plan.get("edits", [])
        room_type = edit_plan.get("room_type", "room")

        if len(edits) == 1:
            # Single edit
            edit = edits[0]
            # Get mask (placeholder - should fetch from Mino)
            mask_data = b""  # TODO: Get actual mask from Mino results

            # Build prompt
            prompt = inference_client._build_edit_prompt(edit, room_type)

            result_image = await inference_client.run_inpainting(
                image_data,
                mask_data,
                prompt,
                strength=edit.get("parameters", {}).get("strength", 0.8),
            )
        else:
            # Multi-edit
            result_image = await inference_client.run_multi_edit(
                image_data, edits, room_type
            )

        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "processing", "progress": 90, "message": "Saving result..."},
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
                },
            )

        return {
            "version_id": version.id,
            "image_url": result_url,
            "processing_time": processing_time,
        }

    except Exception as e:
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "error", "message": f"Edit failed: {str(e)}"},
            )
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
