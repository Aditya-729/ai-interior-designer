"""
Client for communicating with the inference service.
"""

import httpx
from app.core.config import settings
from typing import Dict, Any, List
import base64
import logging

logger = logging.getLogger(__name__)


class InferenceClient:
    """Client for inference service API."""

    def __init__(self):
        self.base_url = settings.INFERENCE_SERVICE_URL
        self.timeout = 300.0
        self.max_retries = 2

    async def run_multi_edit(
        self,
        image_data: bytes,
        edits: List[Dict[str, Any]],
        room_type: str,
    ) -> bytes:
        """
        Run multiple edits via inference service.

        Args:
            image_data: Original image bytes
            edits: List of edit instructions
            room_type: Room type for context

        Returns:
            Final edited image bytes
        """
        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode("utf-8")

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/generate",
                        json={
                            "image": image_b64,
                            "edits": edits,
                            "room_type": room_type,
                        },
                    )
                    response.raise_for_status()
                    result = response.json()

                    # Decode result image
                    result_image_b64 = result["image"]
                    return base64.b64decode(result_image_b64)
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                    logger.warning(f"Inference service error, retrying ({attempt + 1}/{self.max_retries}): {e}")
                    continue
                raise
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Inference service timeout, retrying ({attempt + 1}/{self.max_retries})")
                    continue
                raise


async def check_inference_service() -> str:
    """Check if inference service is available."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.INFERENCE_SERVICE_URL}/health")
            response.raise_for_status()
            return "connected"
    except Exception:
        return "disconnected"


inference_client = InferenceClient()
