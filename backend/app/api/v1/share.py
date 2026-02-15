"""
Public share endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.version import Version
from app.db.models.project import Project
from app.db.models.image import Image
from app.middleware.auth import require_auth
import secrets
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/projects/{project_id}/share")
async def create_share_link(
    project_id: str,
    version_id: str = Body(...),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Create public share link for a version.
    
    Returns:
        {"share_token": "...", "share_url": "..."}
    """
    # Require authentication
    user_id = await require_auth(request)
    
    # Verify project ownership
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Verify version belongs to project
    version = db.query(Version).filter(
        Version.id == version_id,
        Version.project_id == project_id
    ).first()
    
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Generate share token
    share_token = secrets.token_urlsafe(16)
    version.share_token = share_token
    version.is_public = True
    db.commit()
    
    from app.core.config import settings
    share_url = f"{settings.public_frontend_url}/share/{share_token}"
    
    logger.info(f"Share link created: {share_token} for version {version_id}")
    
    return {
        "share_token": share_token,
        "share_url": share_url,
    }


@router.get("/share/{share_token}")
async def get_shared_version(
    share_token: str,
    db: Session = Depends(get_db),
):
    """
    Get shared version data (no auth required).
    
    Returns:
        {
            "version": {...},
            "project": {...},
            "original_image": "...",
            "edited_image": "...",
            "edit_plan": {...}
        }
    """
    version = db.query(Version).filter(
        Version.share_token == share_token,
        Version.is_public == True
    ).first()
    
    if not version:
        raise HTTPException(status_code=404, detail="Share link not found or expired")
    
    # Get project
    project = db.query(Project).filter(Project.id == version.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get original image
    images = db.query(Image).filter(Image.project_id == version.project_id).all()
    original_image = images[0].original_url if images else None
    
    return {
        "version": {
            "id": version.id,
            "image_url": version.image_url,
            "user_prompt": version.user_prompt,
            "created_at": version.created_at,
        },
        "project": {
            "name": project.name,
            "description": project.description,
            "room_type": project.room_type,
        },
        "original_image": original_image,
        "edited_image": version.image_url,
        "edit_plan": version.edit_plan,
    }
