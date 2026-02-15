"""
Design knowledge endpoints using Perplexity AI.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.image import Image
from app.services.perplexity_client import perplexity_client
from app.services.mino_client import mino_client
from app.services.vector_memory import vector_memory
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/fetch-design-knowledge")
async def fetch_design_knowledge(
    user_request: str = Body(...),
    image_id: str = Body(...),
    project_id: Optional[str] = Body(None),
    db: Session = Depends(get_db),
):
    """
    Get design recommendations from Perplexity AI.
    
    Calls Perplexity API and stores references in vector memory.
    
    Returns:
        Design recommendations and knowledge
    """
    try:
        # Get image
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Analyze scene
        from app.api.v1.scene import analyze_scene
        analysis = await analyze_scene(image_id=image_id, db=db)
        
        # Extract context
        detected_objects = mino_client.extract_detected_objects(analysis)
        object_labels = [obj.get("label", "") for obj in detected_objects]
        room_type = mino_client.extract_room_type(analysis)
        
        # Get user preferences if project_id provided
        context = None
        if project_id:
            # In production, fetch from database
            context = {}
        
        # Get recommendations from Perplexity
        recommendations = await perplexity_client.get_design_recommendations(
            user_request=user_request,
            room_type=room_type,
            detected_objects=object_labels,
            context=context,
        )
        
        # Store in vector memory
        if project_id:
            vector_memory.store_design_reference(
                project_id=project_id,
                user_prompt=user_request,
                edit_plan={},  # Would include edit plan if available
                room_type=room_type,
                metadata={"recommendations": recommendations},
            )
        
        logger.info(f"Design knowledge fetched: {image_id}")
        
        return recommendations
    except Exception as e:
        logger.error(f"Failed to fetch design knowledge: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch design knowledge: {str(e)}")
