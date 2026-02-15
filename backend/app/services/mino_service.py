"""
Mino AI API integration for scene understanding and object detection.
"""

import httpx
from app.config import settings
from typing import Dict, List, Any
import base64


class MinoService:
    """Service for interacting with Mino AI API."""

    def __init__(self):
        self.api_key = settings.mino_ai_api_key
        self.base_url = "https://api.mino.ai/v1"  # Adjust based on actual Mino API

    async def analyze_scene(
        self, image_data: bytes, image_format: str = "jpeg"
    ) -> Dict[str, Any]:
        """
        Analyze scene and detect objects.

        Returns:
            {
                "room_type": "living_room",
                "objects": [
                    {
                        "label": "wall",
                        "confidence": 0.95,
                        "bbox": [x1, y1, x2, y2],
                        "mask": "base64_encoded_mask",
                        "category": "structural"
                    },
                    ...
                ],
                "layout": {
                    "walls": [...],
                    "floor": {...},
                    "ceiling": {...}
                }
            }
        """
        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode("utf-8")

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/analyze",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "image": image_b64,
                    "format": image_format,
                    "tasks": ["object_detection", "segmentation", "room_classification"],
                },
            )
            response.raise_for_status()
            return response.json()

    async def get_segmentation_masks(
        self, image_data: bytes, objects: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get segmentation masks for specific objects.

        Args:
            image_data: Image bytes
            objects: List of object labels to segment (e.g., ["wall", "floor", "sofa"])

        Returns:
            Dictionary mapping object labels to mask data
        """
        analysis = await self.analyze_scene(image_data)

        masks = {}
        for obj in analysis.get("objects", []):
            label = obj.get("label")
            if objects is None or label in objects:
                masks[label] = {
                    "mask": obj.get("mask"),
                    "bbox": obj.get("bbox"),
                    "confidence": obj.get("confidence"),
                }

        return masks

    def extract_room_type(self, analysis: Dict[str, Any]) -> str:
        """Extract room type from analysis."""
        return analysis.get("room_type", "unknown")

    def extract_detected_objects(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract detected objects list."""
        return analysis.get("objects", [])


mino_service = MinoService()
