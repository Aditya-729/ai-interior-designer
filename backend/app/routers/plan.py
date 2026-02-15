"""
Edit planning endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.planner import planner
from app.services.mino_service import mino_service
from app.models import Project, UserPreferences
from typing import Optional, Dict, Any

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

    Args:
        user_prompt: User's natural language request
        image_id: Image to edit
        project_id: Optional project ID for context

    Returns:
        Structured edit plan
    """
    # Get scene analysis
    from app.routers.analyze import analyze_scene

    try:
        analysis = await analyze_scene(image_id=image_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze scene: {str(e)}"
        )

    # Get user preferences if project_id provided
    user_preferences = None
    if project_id:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.user_id:
            prefs = (
                db.query(UserPreferences)
                .filter(UserPreferences.user_id == project.user_id)
                .first()
            )
            if prefs:
                user_preferences = {
                    "preferred_colors": prefs.preferred_colors or [],
                    "preferred_materials": prefs.preferred_materials or [],
                    "preferred_styles": prefs.preferred_styles or [],
                }

    # Extract detected objects
    detected_objects = mino_service.extract_detected_objects(analysis)
    room_type = mino_service.extract_room_type(analysis)

    # Plan edits
    try:
        edit_plan = await planner.plan_edits(
            user_prompt, detected_objects, room_type, user_preferences
        )
        return edit_plan
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Edit planning failed: {str(e)}"
        )
