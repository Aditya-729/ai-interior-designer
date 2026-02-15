"""
Mask utilities for processing segmentation masks.
"""

from PIL import Image
from typing import Dict, Any, Tuple
import base64
import io
import logging

logger = logging.getLogger(__name__)


class MaskUtils:
    """Utilities for mask processing."""

    def __init__(self):
        pass

    def get_mask_for_edit(self, edit: Dict[str, Any], image_size: Tuple[int, int]) -> Image.Image:
        """
        Get mask for edit operation.
        
        Args:
            edit: Edit instruction with mask data
            image_size: Target image size (width, height)
            
        Returns:
            PIL Image mask (white = inpaint, black = keep)
        """
        # Check if mask is provided in edit
        mask_data = edit.get("mask")
        mask_id = edit.get("mask_id")
        
        if mask_data:
            # Decode base64 mask
            try:
                mask_bytes = base64.b64decode(mask_data)
                mask = Image.open(io.BytesIO(mask_bytes)).convert("L")
                # Resize to image size
                mask = mask.resize(image_size, Image.LANCZOS)
                return mask
            except Exception as e:
                logger.warning(f"Failed to decode mask: {e}, using full mask")
        
        # If no mask provided, create a full mask (inpaint everything)
        # In production, this should fetch from Mino results stored in database
        logger.warning(f"No mask provided for edit, using full mask")
        mask = Image.new("L", image_size, 255)  # White = inpaint everything
        return mask

    def combine_masks(self, masks: list[Image.Image]) -> Image.Image:
        """Combine multiple masks into one."""
        if not masks:
            raise ValueError("No masks provided")
        
        # Use first mask as base
        combined = masks[0].copy()
        
        # Combine with other masks (union)
        for mask in masks[1:]:
            # Ensure same size
            if mask.size != combined.size:
                mask = mask.resize(combined.size, Image.LANCZOS)
            # Combine (take maximum)
            from PIL import ImageChops
            combined = ImageChops.lighter(combined, mask)
        
        return combined

    def resize_mask(self, mask: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """Resize mask to target size."""
        return mask.resize(target_size, Image.LANCZOS)
