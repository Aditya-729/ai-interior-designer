"""
Command planner - converts user requests into structured edit instructions.
"""

from typing import Dict, List, Any, Optional
from app.services.perplexity_service import perplexity_service
import json
import re


class EditPlanner:
    """Planner that converts natural language to structured edit plans."""

    # Object synonyms mapping
    OBJECT_SYNONYMS = {
        "wall": ["wall", "walls", "wall surface"],
        "floor": ["floor", "ground", "flooring", "tiles", "tile"],
        "ceiling": ["ceiling", "ceiling surface"],
        "sofa": ["sofa", "couch", "settee"],
        "bed": ["bed", "mattress"],
        "table": ["table", "desk", "dining table"],
        "cabinet": ["cabinet", "cupboard", "wardrobe"],
        "window": ["window", "windows"],
        "door": ["door", "doors"],
        "lamp": ["lamp", "light", "lighting", "lights"],
    }

    # Operation types
    OPERATIONS = {
        "recolor": ["color", "colour", "paint", "make", "change color", "recolor"],
        "texture": ["texture", "material", "change material", "replace"],
        "lighting": ["light", "lighting", "illumination", "brightness"],
    }

    def __init__(self):
        pass

    async def plan_edits(
        self,
        user_prompt: str,
        detected_objects: List[Dict[str, Any]],
        room_type: str,
        user_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create structured edit plan from user request.

        Args:
            user_prompt: User's natural language request
            detected_objects: List of detected objects from Mino
            room_type: Type of room
            user_preferences: User's style preferences

        Returns:
            {
                "edits": [
                    {
                        "target_object": "wall",
                        "operation": "recolor",
                        "parameters": {
                            "color": "warm beige",
                            "strength": 0.8
                        },
                        "mask_id": "wall_mask_123"
                    },
                    ...
                ],
                "validation": {
                    "valid": true,
                    "warnings": [...]
                }
            }
        """
        # Normalize detected objects
        available_objects = self._normalize_objects(detected_objects)

        # Extract edit requests from prompt
        edit_requests = self._parse_prompt(user_prompt)

        # Validate and map to detected objects
        validated_edits = self._validate_and_map(edit_requests, available_objects)

        # Enrich with design knowledge if needed
        if user_preferences:
            validated_edits = self._apply_preferences(validated_edits, user_preferences)

        # Build final plan
        plan = {
            "edits": validated_edits,
            "validation": self._validate_plan(validated_edits),
            "room_type": room_type,
            "original_prompt": user_prompt,
        }

        return plan

    def _normalize_objects(self, detected_objects: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Normalize detected objects into a searchable dictionary."""
        normalized = {}
        for obj in detected_objects:
            label = obj.get("label", "").lower()
            # Map synonyms
            for key, synonyms in self.OBJECT_SYNONYMS.items():
                if label in synonyms or any(syn in label for syn in synonyms):
                    normalized[key] = obj
                    break
            else:
                normalized[label] = obj
        return normalized

    def _parse_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """Parse user prompt into edit requests."""
        prompt_lower = prompt.lower()
        edits = []

        # Pattern matching for common requests
        # Example: "make the wall warm beige"
        color_pattern = r"(?:make|change|paint|color|colour)\s+(?:the\s+)?(\w+)\s+(?:to|as|in)?\s+([\w\s]+?)(?:,|\.|$)"
        matches = re.finditer(color_pattern, prompt_lower)

        for match in matches:
            object_name = match.group(1)
            color_desc = match.group(2).strip()
            edits.append(
                {
                    "target_object": object_name,
                    "operation": "recolor",
                    "parameters": {"color": color_desc},
                }
            )

        # Pattern for material changes: "change floor tiles to marble"
        material_pattern = r"(?:change|replace|make)\s+(?:the\s+)?(\w+)\s+(?:tiles?|material|texture)?\s+(?:to|with|as)\s+([\w\s]+?)(?:,|\.|$)"
        matches = re.finditer(material_pattern, prompt_lower)

        for match in matches:
            object_name = match.group(1)
            material = match.group(2).strip()
            edits.append(
                {
                    "target_object": object_name,
                    "operation": "texture",
                    "parameters": {"material": material},
                }
            )

        # Pattern for lighting: "add warm ceiling lights"
        lighting_pattern = r"(?:add|change|make)\s+([\w\s]+?)\s+(?:light|lighting|lights?)(?:,|\.|$)"
        matches = re.finditer(lighting_pattern, prompt_lower)

        for match in matches:
            light_desc = match.group(1).strip()
            edits.append(
                {
                    "target_object": "ceiling",
                    "operation": "lighting",
                    "parameters": {"style": light_desc},
                }
            )

        # If no patterns matched, try to extract general intent
        if not edits:
            edits.append(
                {
                    "target_object": "unknown",
                    "operation": "general",
                    "parameters": {"prompt": prompt},
                }
            )

        return edits

    def _validate_and_map(
        self, edit_requests: List[Dict[str, Any]], available_objects: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Validate edit requests against detected objects."""
        validated = []

        for edit in edit_requests:
            target = edit["target_object"].lower()

            # Try to find matching object
            matched_obj = None
            for obj_key, obj_data in available_objects.items():
                if target in obj_key or obj_key in target:
                    matched_obj = obj_data
                    break

            # Try synonyms
            if not matched_obj:
                for key, synonyms in self.OBJECT_SYNONYMS.items():
                    if target in synonyms:
                        matched_obj = available_objects.get(key)
                        if matched_obj:
                            target = key
                            break

            if matched_obj:
                validated.append(
                    {
                        "target_object": target,
                        "operation": edit["operation"],
                        "parameters": edit["parameters"],
                        "mask_id": matched_obj.get("id"),
                        "confidence": matched_obj.get("confidence", 0.5),
                    }
                )
            else:
                # Fallback: try to infer from context
                validated.append(
                    {
                        "target_object": target,
                        "operation": edit["operation"],
                        "parameters": edit["parameters"],
                        "mask_id": None,
                        "confidence": 0.3,
                        "warning": f"Object '{target}' not detected, will attempt inference",
                    }
                )

        return validated

    def _apply_preferences(
        self, edits: List[Dict[str, Any]], preferences: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Apply user preferences to edits."""
        preferred_colors = preferences.get("preferred_colors", [])
        preferred_materials = preferences.get("preferred_materials", [])

        for edit in edits:
            params = edit.get("parameters", {})
            if "color" in params and not params["color"]:
                if preferred_colors:
                    params["color"] = preferred_colors[0]
            if "material" in params and not params["material"]:
                if preferred_materials:
                    params["material"] = preferred_materials[0]

        return edits

    def _validate_plan(self, edits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate the complete edit plan."""
        warnings = []
        valid = True

        if not edits:
            valid = False
            warnings.append("No valid edits found in request")

        low_confidence_count = sum(1 for e in edits if e.get("confidence", 1.0) < 0.5)
        if low_confidence_count > 0:
            warnings.append(f"{low_confidence_count} edits have low confidence")

        missing_masks = sum(1 for e in edits if e.get("mask_id") is None)
        if missing_masks > 0:
            warnings.append(f"{missing_masks} edits missing segmentation masks")

        return {"valid": valid, "warnings": warnings}


planner = EditPlanner()
