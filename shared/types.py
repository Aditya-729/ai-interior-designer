"""
Shared type definitions for the project.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class EditInstruction(BaseModel):
    """Single edit instruction."""
    target_object: str
    operation: str  # "recolor", "texture", "lighting"
    parameters: Dict[str, Any]
    mask_id: Optional[str] = None
    confidence: float = 1.0


class EditPlan(BaseModel):
    """Complete edit plan."""
    edits: List[EditInstruction]
    validation: Dict[str, Any]
    room_type: str
    original_prompt: str


class DetectedObject(BaseModel):
    """Detected object from scene analysis."""
    label: str
    confidence: float
    bbox: List[float]
    mask: Optional[str] = None
    category: str


class SceneAnalysis(BaseModel):
    """Scene analysis result."""
    room_type: str
    objects: List[DetectedObject]
    layout: Dict[str, Any]
