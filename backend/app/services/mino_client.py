"""
Mino AI API client for scene understanding and object detection.
"""

import httpx
from app.core.config import settings
from typing import Dict, List, Any, Optional
import base64
import logging

logger = logging.getLogger(__name__)


class MinoClient:
    """Client for Mino AI API."""

    def __init__(self):
        self.api_key = settings.MINO_AI_API_KEY
        self.base_url = "https://api.mino.ai/v1"  # Adjust based on actual Mino API
        self.timeout = 60.0
        self.max_retries = 3

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

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
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
                    result = response.json()
                    logger.info(f"Mino analysis successful: room_type={result.get('room_type')}")
                    return result
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                    logger.warning(f"Mino API error, retrying ({attempt + 1}/{self.max_retries}): {e}")
                    continue
                raise
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Mino API timeout, retrying ({attempt + 1}/{self.max_retries})")
                    continue
                raise

    async def get_segmentation_masks(
        self, image_data: bytes, objects: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get segmentation masks for specific objects.

        Args:
            image_data: Image bytes
            objects: List of object labels to segment

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


mino_client = MinoClient()
