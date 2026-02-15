"""
Perplexity AI API integration for design knowledge and recommendations.
"""

import httpx
from app.config import settings
from typing import Dict, List, Any, Optional


class PerplexityService:
    """Service for interacting with Perplexity AI API."""

    def __init__(self):
        self.api_key = settings.perplexity_api_key
        self.base_url = "https://api.perplexity.ai/chat/completions"

    async def get_design_recommendations(
        self,
        user_request: str,
        room_type: str,
        detected_objects: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get design recommendations from Perplexity.

        Args:
            user_request: User's design request
            room_type: Type of room (living_room, bedroom, etc.)
            detected_objects: List of detected objects in the scene
            context: Additional context (user preferences, existing colors, etc.)

        Returns:
            {
                "recommendations": [...],
                "color_harmony": {...},
                "material_compatibility": {...},
                "lighting_suggestions": [...],
                "trends": [...],
                "safety_considerations": [...]
            }
        """
        prompt = self._build_prompt(user_request, room_type, detected_objects, context)

        async with httpx.AsyncClient(timeout=30.0) as client:
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
            return self._parse_response(content)

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
            # You could add more sophisticated parsing here
        }

    async def get_color_harmony(
        self, base_color: str, room_type: str
    ) -> Dict[str, List[str]]:
        """Get color harmony suggestions."""
        prompt = (
            f"For a {room_type} with base color {base_color}, "
            "suggest a harmonious color palette with 3-5 complementary colors. "
            "Include specific color names (e.g., 'warm beige', 'navy blue')."
        )

        result = await self.get_design_recommendations(
            prompt, room_type, [], {"query_type": "color_harmony"}
        )

        return {"palette": result.get("recommendations", "")}

    async def get_material_compatibility(
        self, materials: List[str], room_type: str
    ) -> Dict[str, Any]:
        """Get material compatibility recommendations."""
        prompt = (
            f"For a {room_type}, assess compatibility of these materials: {', '.join(materials)}. "
            "Consider durability, maintenance, and aesthetic harmony."
        )

        result = await self.get_design_recommendations(
            prompt, room_type, [], {"query_type": "material_compatibility"}
        )

        return {"compatibility": result.get("recommendations", "")}


perplexity_service = PerplexityService()
