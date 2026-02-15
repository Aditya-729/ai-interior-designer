"""
Inference service for GPU-based image editing using Stable Diffusion.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import base64
import io
from PIL import Image
import torch
import os
from dotenv import load_dotenv
import logging

from pipelines.inpaint_pipeline import InpaintPipeline
from pipelines.mask_utils import MaskUtils

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Inference Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline
inpaint_pipeline = None
mask_utils = None


class GenerateRequest(BaseModel):
    image: str  # Base64 encoded
    edits: List[Dict[str, Any]]
    room_type: str


@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    global inpaint_pipeline, mask_utils
    logger.info("Loading inference models...")
    inpaint_pipeline = InpaintPipeline()
    mask_utils = MaskUtils()
    logger.info("Models loaded successfully!")


@app.get("/")
async def root():
    """Health check."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return {
        "status": "ok",
        "service": "Inference Service",
        "device": device,
        "models_loaded": inpaint_pipeline is not None,
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return {
        "status": "healthy",
        "device": device,
        "models_loaded": inpaint_pipeline is not None,
        "cuda_available": torch.cuda.is_available(),
    }


@app.post("/generate")
async def generate(request: GenerateRequest):
    """
    Generate edited image from edit plan.
    
    Accepts:
    - original image (base64)
    - segmentation masks (from edits)
    - edit plan JSON
    
    Runs:
    - Stable Diffusion inpainting
    - Optional ControlNet
    
    Supports:
    - Multi-object edits in one request
    - Chained edits
    
    Returns:
    - Final image (base64)
    - Optional intermediate images
    """
    if inpaint_pipeline is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        # Decode image
        image_data = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process edits
        current_image = image
        for edit in request.edits:
            # Get mask for this edit
            mask = mask_utils.get_mask_for_edit(edit, current_image.size)
            
            # Build prompt
            prompt = _build_edit_prompt(edit, request.room_type)
            
            # Get parameters
            strength = edit.get("strength", 0.8)
            
            # Run inpainting
            current_image = await inpaint_pipeline.inpaint(
                image=current_image,
                mask=mask,
                prompt=prompt,
                strength=strength,
            )

        # Encode result
        buffer = io.BytesIO()
        current_image.save(buffer, format="JPEG", quality=95)
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        logger.info(f"Generation complete: {len(request.edits)} edits")

        return {"image": result_b64}

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


def _build_edit_prompt(edit: Dict[str, Any], room_type: str) -> str:
    """Build prompt for a single edit."""
    target = edit.get("object", "room")
    operation = edit.get("operation", "general")
    
    if operation == "recolor":
        color = edit.get("color", "")
        return f"{target} in {color} color, {room_type}, realistic, high quality, professional photography"
    elif operation == "texture":
        material = edit.get("material", "")
        return f"{target} with {material} texture, {room_type}, realistic, high quality, professional photography"
    elif operation == "lighting":
        style = edit.get("style", "")
        return f"{target} with {style} lighting, {room_type}, realistic, high quality, professional photography"
    else:
        return f"{target} in {room_type}, realistic, high quality, professional photography"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
