"""
Image and audio upload endpoints.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.image import Image
from app.db.models.project import Project
from app.services.storage import storage
from PIL import Image as PILImage
import io
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    project_id: str = None,
    db: Session = Depends(get_db),
):
    """
    Upload a room image.
    
    Saves original image to S3-compatible storage and creates database row.
    
    Returns:
        {
            "image_id": "...",
            "url": "...",
            "width": 1920,
            "height": 1080,
            "project_id": "..."
        }
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read file
        file_data = await file.read()
        
        # Get image dimensions
        img = PILImage.open(io.BytesIO(file_data))
        width, height = img.size
        
        # Generate storage key
        storage_key = storage.generate_key("images", file.filename or "image.jpg")
        
        # Upload to R2
        image_url = storage.upload_file(
            file_data, storage_key, content_type=file.content_type
        )
        
        # Verify project exists if provided
        if project_id:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
        
        # Save to database
        db_image = Image(
            project_id=project_id,
            original_url=image_url,
            storage_key=storage_key,
            width=width,
            height=height,
            file_size=len(file_data),
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        logger.info(f"Image uploaded: {db_image.id}")
        
        return {
            "image_id": db_image.id,
            "url": image_url,
            "width": width,
            "height": height,
            "project_id": project_id,
            "storage_key": storage_key,
        }
    except Exception as e:
        logger.error(f"Image upload failed: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file for transcription.
    
    Stores audio and returns audio ID.
    
    Returns:
        {
            "audio_id": "...",
            "url": "...",
            "storage_key": "..."
        }
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    try:
        # Read file
        file_data = await file.read()
        
        # Generate storage key
        storage_key = storage.generate_key("audio", file.filename or "audio.webm")
        
        # Upload to R2
        audio_url = storage.upload_file(
            file_data, storage_key, content_type=file.content_type
        )
        
        logger.info(f"Audio uploaded: {storage_key}")
        
        return {
            "audio_id": storage_key,
            "url": audio_url,
            "storage_key": storage_key,
        }
    except Exception as e:
        logger.error(f"Audio upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
