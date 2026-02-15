"""
Design knowledge endpoints using Perplexity AI.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.perplexity_service import perplexity_service
from app.services.mino_service import mino_service
from app.models import Image, Project, UserPreferences
from typing import Optional, List

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

    Args:
        user_request: User's design request
        image_id: Image ID for context
        project_id: Optional project ID

    Returns:
        Design recommendations and knowledge
    """
    # Get scene analysis
    from app.routers.analyze import analyze_scene

    try:
        analysis = await analyze_scene(image_id=image_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to analyze scene: {str(e)}"
        )

    # Extract context
    detected_objects = mino_service.extract_detected_objects(analysis)
    object_labels = [obj.get("label", "") for obj in detected_objects]
    room_type = mino_service.extract_room_type(analysis)

    # Get user preferences
    context = None
    if project_id:
        project = db.query(Project).filter(Project.id == project_id).first()
        if project and project.user_id:
            prefs = (
                db.query(UserPreferences)
                .filter(UserPreferences.user_id == project.user_id)
                .first()
            )
            if prefs:
                context = {
                    "preferred_colors": prefs.preferred_colors or [],
                    "preferred_materials": prefs.preferred_materials or [],
                }

    # Get recommendations
    try:
        recommendations = await perplexity_service.get_design_recommendations(
            user_request, room_type, object_labels, context
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch design knowledge: {str(e)}"
        )


@router.post("/get-color-harmony")
async def get_color_harmony(
    base_color: str = Body(...),
    room_type: str = Body(...),
):
    """Get color harmony suggestions."""
    try:
        result = await perplexity_service.get_color_harmony(base_color, room_type)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get color harmony: {str(e)}"
        )


@router.post("/get-material-compatibility")
async def get_material_compatibility(
    materials: List[str] = Body(...),
    room_type: str = Body(...),
):
    """Get material compatibility recommendations."""
    try:
        result = await perplexity_service.get_material_compatibility(
            materials, room_type
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get material compatibility: {str(e)}",
        )
