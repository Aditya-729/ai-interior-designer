"""
Project management endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project, Image, Version, User
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: str


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    room_type: Optional[str] = None


@router.post("/projects")
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    """Create a new project."""
    # Verify user exists
    user = db.query(User).filter(User.id == project_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=project_data.user_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "user_id": project.user_id,
        "created_at": project.created_at,
    }


@router.get("/projects")
async def list_projects(
    user_id: str,
    db: Session = Depends(get_db),
):
    """List all projects for a user."""
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
    db: Session = Depends(get_db),
):
    """Get project details with images and versions."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

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


@router.patch("/projects/{project_id}")
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
):
    """Update project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_data.name:
        project.name = project_data.name
    if project_data.description is not None:
        project.description = project_data.description
    if project_data.room_type:
        project.room_type = project_data.room_type

    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "room_type": project.room_type,
    }


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
):
    """Delete project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted"}
