"""
Edit planning endpoint.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.image import Image
from app.services.planner_service import planner_service
from app.services.mino_client import mino_client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/plan-edits")
async def plan_edits(
    user_prompt: str = Body(...),
    image_id: str = Body(...),
    project_id: Optional[str] = Body(None),
    db: Session = Depends(get_db),
):
    """
    Generate structured edit plan from user request.
    
    Input:
    - user text
    - scene objects
    - room type
    - past preferences
    
    Output strict JSON plan:
    {
        "room_type": "...",
        "edits": [
            {
                "object": "wall",
                "operation": "recolor",
                "style": "...",
                "color": "...",
                "material": "...",
                "strength": 0.7
            }
        ]
    }
    """
    try:
        # Get image
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Analyze scene if not already done (in production, cache this)
        from app.api.v1.scene import analyze_scene
        analysis = await analyze_scene(image_id=image_id, db=db)
        
        # Extract context
        detected_objects = mino_client.extract_detected_objects(analysis)
        room_type = mino_client.extract_room_type(analysis)
        
        # Get user preferences if project_id provided
        user_preferences = None
        if project_id:
            # In production, fetch from database
            # For now, use empty preferences
            user_preferences = {}
        
        # Plan edits
        edit_plan = await planner_service.plan_edits(
            user_prompt=user_prompt,
            detected_objects=detected_objects,
            room_type=room_type,
            user_preferences=user_preferences,
        )
        
        logger.info(f"Edit plan generated: {image_id}, edits={len(edit_plan.get('edits', []))}")
        
        return edit_plan
    except Exception as e:
        logger.error(f"Edit planning failed: {e}")
        raise HTTPException(status_code=500, detail=f"Edit planning failed: {str(e)}")
