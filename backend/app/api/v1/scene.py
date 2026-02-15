"""
Scene analysis endpoints using Mino AI.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.image import Image
from app.services.mino_client import mino_client
from app.services.storage import storage
import httpx
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/analyze-scene")
async def analyze_scene(
    image_id: str = Body(...),
    db: Session = Depends(get_db),
):
    """
    Analyze scene using Mino API.
    
    Calls Mino API and stores:
    - Detected objects
    - Masks / regions
    - Scene type
    
    Returns:
        {
            "room_type": "living_room",
            "objects": [...],
            "layout": {...}
        }
    """
    try:
        # Get image from database
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Download image
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(db_image.original_url)
            response.raise_for_status()
            image_data = response.content
        
        # Analyze with Mino
        analysis = await mino_client.analyze_scene(image_data)
        
        logger.info(f"Scene analyzed: {image_id}, room_type={analysis.get('room_type')}, objects={len(analysis.get('objects', []))}")
        
        return analysis
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during scene analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download image: {str(e)}")
    except Exception as e:
        logger.error(f"Scene analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scene analysis failed: {str(e)}")


@router.post("/get-segmentation-masks")
async def get_segmentation_masks(
    image_id: str = Body(...),
    objects: list[str] = Body(None),
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
    try:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")

        # Download image
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(db_image.original_url)
            response.raise_for_status()
            image_data = response.content

        # Get masks
        masks = await mino_client.get_segmentation_masks(image_data, objects)
        
        logger.info(f"Masks extracted: {image_id}, objects={len(masks)}")
        
        return masks
    except Exception as e:
        logger.error(f"Mask extraction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Mask extraction failed: {str(e)}")
