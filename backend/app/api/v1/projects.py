"""
Project management endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.project import Project
from app.db.models.user import User
from app.db.models.image import Image
from app.db.models.version import Version
from app.middleware.auth import require_auth, get_current_user_id
from app.services.usage_limiter import UsageLimiter
from typing import Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


@router.post("/projects")
async def create_project(
    project_data: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """Create a new project."""
    # Require authentication
    user_id = await require_auth(request)
    
    # Check project limit
    limiter = UsageLimiter(db)
    allowed, message = limiter.check_project_limit(user_id)
    if not allowed:
        raise HTTPException(status_code=403, detail=message)
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=user_id,  # Use authenticated user ID
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    logger.info(f"Project created: {project.id} by user {user_id}")

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
    }


@router.get("/projects")
async def list_projects(
    request: Request,
    db: Session = Depends(get_db),
):
    """List all projects for authenticated user."""
    user_id = await require_auth(request)
    projects = db.query(Project).filter(Project.user_id == user_id).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "room_type": p.room_type,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
        }
        for p in projects
    ]


@router.get("/projects/{project_id}")
async def get_project(
    project_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """Get project details with images and versions."""
    user_id = await require_auth(request)
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check ownership
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    images = db.query(Image).filter(Image.project_id == project_id).all()
    versions = db.query(Version).filter(Version.project_id == project_id).all()

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "room_type": project.room_type,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "images": [
            {
                "id": img.id,
                "url": img.original_url,
                "width": img.width,
                "height": img.height,
            }
            for img in images
        ],
        "versions": [
            {
                "id": v.id,
                "image_url": v.image_url,
                "created_at": v.created_at,
                "user_prompt": v.user_prompt,
            }
            for v in versions
        ],
    }
