"""
Scene analysis endpoints using Mino AI.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.mino_service import mino_service
from app.storage import storage
from app.models import Image
import httpx

router = APIRouter()


@router.post("/analyze-scene")
async def analyze_scene(
    image_id: str = None,
    image_url: str = None,
    db: Session = Depends(get_db),
):
    """
    Analyze scene using Mino AI API.

    Args:
        image_id: Database image ID
        image_url: Direct image URL

    Returns:
        {
            "room_type": "living_room",
            "objects": [...],
            "layout": {...}
        }
    """
    # Get image data
    image_data = None
    if image_id:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")
        image_url = db_image.original_url

    if image_url:
        # Download image
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
            response.raise_for_status()
            image_data = response.content
    else:
        raise HTTPException(
            status_code=400, detail="Either image_id or image_url must be provided"
        )

    # Analyze with Mino
    try:
        analysis = await mino_service.analyze_scene(image_data)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Scene analysis failed: {str(e)}"
        )


@router.post("/get-segmentation-masks")
async def get_segmentation_masks(
    image_id: str,
    objects: list[str] = None,
    db: Session = Depends(get_db),
):
    """
    Get segmentation masks for specific objects.

    Args:
        image_id: Database image ID
        objects: List of object labels to segment

    Returns:
        Dictionary mapping object labels to masks
    """
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Download image
    async with httpx.AsyncClient() as client:
        response = await client.get(db_image.original_url)
        response.raise_for_status()
        image_data = response.content

    # Get masks
    try:
        masks = await mino_service.get_segmentation_masks(image_data, objects)
        return masks
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Mask extraction failed: {str(e)}"
        )
