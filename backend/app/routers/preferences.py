"""
User preferences endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserPreferences, User
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()


class PreferencesUpdate(BaseModel):
    preferred_colors: Optional[List[str]] = None
    preferred_materials: Optional[List[str]] = None
    preferred_styles: Optional[List[str]] = None
    room_type_preferences: Optional[dict] = None


@router.get("/preferences/{user_id}")
async def get_preferences(
    user_id: str,
    db: Session = Depends(get_db),
):
    """Get user preferences."""
    prefs = (
        db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    )

    if not prefs:
        # Create default preferences
        prefs = UserPreferences(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)

    return {
        "user_id": prefs.user_id,
        "preferred_colors": prefs.preferred_colors or [],
        "preferred_materials": prefs.preferred_materials or [],
        "preferred_styles": prefs.preferred_styles or [],
        "room_type_preferences": prefs.room_type_preferences or {},
    }


@router.put("/preferences/{user_id}")
async def update_preferences(
    user_id: str,
    preferences: PreferencesUpdate,
    db: Session = Depends(get_db),
):
    """Update user preferences."""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    prefs = (
        db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    )

    if not prefs:
        prefs = UserPreferences(user_id=user_id)
        db.add(prefs)

    if preferences.preferred_colors is not None:
        prefs.preferred_colors = preferences.preferred_colors
    if preferences.preferred_materials is not None:
        prefs.preferred_materials = preferences.preferred_materials
    if preferences.preferred_styles is not None:
        prefs.preferred_styles = preferences.preferred_styles
    if preferences.room_type_preferences is not None:
        prefs.room_type_preferences = preferences.room_type_preferences

    db.commit()
    db.refresh(prefs)

    return {
        "user_id": prefs.user_id,
        "preferred_colors": prefs.preferred_colors or [],
        "preferred_materials": prefs.preferred_materials or [],
        "preferred_styles": prefs.preferred_styles or [],
        "room_type_preferences": prefs.room_type_preferences or {},
    }
