"""
Stable Diffusion inpainting pipeline.
"""

import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)


class InpaintPipeline:
    """Stable Diffusion inpainting pipeline."""

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_id = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-inpainting")
        self.model_path = os.getenv("INFERENCE_MODEL_PATH", "./models")
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        """Load Stable Diffusion model."""
        logger.info(f"Loading Stable Diffusion model: {self.model_id}")
        logger.info(f"Device: {self.device}")
        
        try:
            self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
                cache_dir=os.path.join(self.model_path, "sd-inpainting"),
            )
            self.pipeline = self.pipeline.to(self.device)
            self.pipeline.enable_attention_slicing()  # Reduce memory usage
            
            if self.device.type == "cuda":
                try:
                    self.pipeline.enable_model_cpu_offload()  # Further memory optimization
                except:
                    pass  # Fallback if not supported
            
            logger.info("Stable Diffusion model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    async def inpaint(
        self,
        image: Image.Image,
        mask: Image.Image,
        prompt: str,
        negative_prompt: str = "blurry, distorted, low quality, artifacts",
        strength: float = 0.8,
        guidance_scale: float = 7.5,
        num_inference_steps: int = 50,
        seed: Optional[int] = None,
    ) -> Image.Image:
        """
        Run inpainting on image with mask.

        Args:
            image: Original image
            mask: Mask image (white = inpaint, black = keep)
            prompt: Text prompt
            negative_prompt: Negative prompt
            strength: Inpainting strength (0-1)
            guidance_scale: Guidance scale
            num_inference_steps: Number of inference steps
            seed: Random seed

        Returns:
            Edited image
        """
        if self.pipeline is None:
            raise RuntimeError("Model not loaded")

        # Ensure mask is same size as image
        if image.size != mask.size:
            mask = mask.resize(image.size, Image.LANCZOS)

        # Generate
        generator = (
            torch.Generator(device=self.device).manual_seed(seed)
            if seed is not None
            else None
        )

        try:
            result = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=image,
                mask_image=mask,
                strength=strength,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                generator=generator,
            )

            return result.images[0]
        except Exception as e:
            logger.error(f"Inpainting failed: {e}")
            raise
