"""
Edit history endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import EditHistory, Project
from typing import Optional

router = APIRouter()


@router.get("/history")
async def get_history(
    project_id: str,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """Get edit history for a project."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    history = (
        db.query(EditHistory)
        .filter(EditHistory.project_id == project_id)
        .order_by(EditHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": h.id,
            "version_id": h.version_id,
            "user_prompt": h.user_prompt,
            "edit_plan": h.edit_plan,
            "processing_time": h.processing_time,
            "created_at": h.created_at,
        }
        for h in history
    ]


@router.get("/history/{history_id}")
async def get_history_item(
    history_id: str,
    db: Session = Depends(get_db),
):
    """Get specific history item."""
    history = db.query(EditHistory).filter(EditHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History item not found")

    return {
        "id": history.id,
        "project_id": history.project_id,
        "version_id": history.version_id,
        "user_prompt": history.user_prompt,
        "edit_plan": history.edit_plan,
        "detected_objects": history.detected_objects,
        "design_knowledge": history.design_knowledge,
        "processing_time": history.processing_time,
        "created_at": history.created_at,
    }
