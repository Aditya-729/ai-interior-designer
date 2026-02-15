"""
Upload endpoints for images and audio.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.storage import storage
from app.models import Image, Project
from PIL import Image as PILImage
import io

router = APIRouter()


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    project_id: str = None,
    db: Session = Depends(get_db),
):
    """
    Upload a room image.

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

    # Read file
    file_data = await file.read()

    # Get image dimensions
    img = PILImage.open(io.BytesIO(file_data))
    width, height = img.size

    # Generate storage key
    storage_key = storage.generate_key("images", file.filename)

    # Upload to R2
    image_url = storage.upload_file(
        file_data, storage_key, content_type=file.content_type
    )

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

    return {
        "image_id": db_image.id,
        "url": image_url,
        "width": width,
        "height": height,
        "project_id": project_id,
        "storage_key": storage_key,
    }


@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file for transcription.

    Returns:
        {
            "audio_id": "...",
            "url": "...",
            "duration": 5.2
        }
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    # Read file
    file_data = await file.read()

    # Generate storage key
    storage_key = storage.generate_key("audio", file.filename)

    # Upload to R2
    audio_url = storage.upload_file(
        file_data, storage_key, content_type=file.content_type
    )

    return {
        "audio_id": storage_key,
        "url": audio_url,
        "storage_key": storage_key,
    }
