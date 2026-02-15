"""
Perplexity AI API client for design knowledge and recommendations.
"""

import httpx
from app.core.config import settings
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PerplexityClient:
    """Client for Perplexity AI API."""

    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.timeout = 30.0
        self.max_retries = 3

    async def get_design_recommendations(
        self,
        user_request: str,
        room_type: str,
        detected_objects: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get design recommendations from Perplexity.

        Returns:
            {
                "recommendations": "...",
                "color_harmony": {...},
                "material_compatibility": {...},
                "lighting_suggestions": [...],
                "trends": [...],
                "safety_considerations": [...]
            }
        """
        prompt = self._build_prompt(user_request, room_type, detected_objects, context)

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "llama-3.1-sonar-large-128k-online",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": (
                                        "You are an expert interior designer. Provide practical, "
                                        "aesthetically sound design recommendations. Focus on color harmony, "
                                        "material compatibility, lighting, and modern trends. Always consider "
                                        "safety and spacing requirements."
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": prompt,
                                },
                            ],
                            "temperature": 0.7,
                            "max_tokens": 2000,
                        },
                    )
                    response.raise_for_status()
                    result = response.json()

                    # Parse the response
                    content = result["choices"][0]["message"]["content"]
                    logger.info(f"Perplexity response received: {len(content)} characters")
                    return self._parse_response(content)
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                    logger.warning(f"Perplexity API error, retrying ({attempt + 1}/{self.max_retries}): {e}")
                    continue
                raise
            except httpx.TimeoutException:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Perplexity API timeout, retrying ({attempt + 1}/{self.max_retries})")
                    continue
                raise

    def _build_prompt(
        self,
        user_request: str,
        room_type: str,
        detected_objects: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build prompt for Perplexity."""
        prompt_parts = [
            f"Room type: {room_type}",
            f"User request: {user_request}",
            f"Detected objects in room: {', '.join(detected_objects)}",
        ]

        if context:
            if context.get("preferred_colors"):
                prompt_parts.append(
                    f"User's preferred colors: {', '.join(context['preferred_colors'])}"
                )
            if context.get("preferred_materials"):
                prompt_parts.append(
                    f"User's preferred materials: {', '.join(context['preferred_materials'])}"
                )

        prompt_parts.append(
            "Provide recommendations for:"
            "\n1. Color harmony and palette suggestions"
            "\n2. Material compatibility"
            "\n3. Lighting recommendations"
            "\n4. Modern design trends"
            "\n5. Safety and spacing considerations"
            "\n\nFormat your response as structured recommendations."
        )

        return "\n".join(prompt_parts)

    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Parse Perplexity response into structured format."""
        # In a real implementation, you might use JSON parsing or structured output
        # For now, return a simple structure
        return {
            "recommendations": content,
            "raw_response": content,
        }


perplexity_client = PerplexityClient()
