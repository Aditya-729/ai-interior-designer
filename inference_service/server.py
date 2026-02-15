"""
Inference service for GPU-based image editing using Stable Diffusion.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import base64
import io
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline, ControlNetModel, StableDiffusionControlNetInpaintPipeline
from controlnet_aux import CannyDetector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Inference Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
inpaint_pipeline = None
controlnet_pipeline = None
canny_detector = None
device = None


class InpaintRequest(BaseModel):
    image: str  # Base64 encoded
    mask: str  # Base64 encoded
    prompt: str
    negative_prompt: Optional[str] = None
    strength: float = 0.8
    guidance_scale: float = 7.5
    num_inference_steps: int = 50
    seed: Optional[int] = None


class MultiEditRequest(BaseModel):
    image: str  # Base64 encoded
    edits: List[Dict[str, Any]]
    room_type: str


def load_models():
    """Load Stable Diffusion models."""
    global inpaint_pipeline, controlnet_pipeline, canny_detector, device

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model_path = os.getenv("INFERENCE_MODEL_PATH", "./models")
    sd_model_id = os.getenv("SD_MODEL_ID", "runwayml/stable-diffusion-inpainting")
    controlnet_model_id = os.getenv(
        "CONTROLNET_MODEL_ID", "lllyasviel/sd-controlnet-canny"
    )

    print("Loading Stable Diffusion Inpainting model...")
    inpaint_pipeline = StableDiffusionInpaintPipeline.from_pretrained(
        sd_model_id,
        torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
        cache_dir=os.path.join(model_path, "sd-inpainting"),
    )
    inpaint_pipeline = inpaint_pipeline.to(device)
    inpaint_pipeline.enable_attention_slicing()  # Reduce memory usage

    print("Loading ControlNet...")
    controlnet = ControlNetModel.from_pretrained(
        controlnet_model_id,
        torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
        cache_dir=os.path.join(model_path, "controlnet-canny"),
    )

    controlnet_pipeline = StableDiffusionControlNetInpaintPipeline.from_pretrained(
        sd_model_id,
        controlnet=controlnet,
        torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
    )
    controlnet_pipeline = controlnet_pipeline.to(device)
    controlnet_pipeline.enable_attention_slicing()

    print("Loading Canny detector...")
    canny_detector = CannyDetector()

    print("Models loaded successfully!")


@app.on_event("startup")
async def startup_event():
    """Load models on startup."""
    load_models()


@app.get("/")
async def root():
    """Health check."""
    return {
        "status": "ok",
        "service": "Inference Service",
        "device": str(device) if device else "not_loaded",
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "device": str(device) if device else "not_loaded",
        "models_loaded": inpaint_pipeline is not None,
    }


@app.post("/inpaint")
async def inpaint(request: InpaintRequest):
    """
    Run inpainting on image with mask.

    Args:
        request: InpaintRequest with image, mask, and parameters

    Returns:
        {
            "image": "base64_encoded_result_image"
        }
    """
    if inpaint_pipeline is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        # Decode images
        image_data = base64.b64decode(request.image)
        mask_data = base64.b64decode(request.mask)

        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        mask = Image.open(io.BytesIO(mask_data)).convert("L")

        # Resize to ensure dimensions match
        if image.size != mask.size:
            mask = mask.resize(image.size, Image.LANCZOS)

        # Generate
        generator = (
            torch.Generator(device=device).manual_seed(request.seed)
            if request.seed is not None
            else None
        )

        result = inpaint_pipeline(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            image=image,
            mask_image=mask,
            strength=request.strength,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps,
            generator=generator,
        )

        result_image = result.images[0]

        # Encode result
        buffer = io.BytesIO()
        result_image.save(buffer, format="JPEG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"image": result_b64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inpainting failed: {str(e)}")


@app.post("/inpaint-with-controlnet")
async def inpaint_with_controlnet(request: InpaintRequest):
    """
    Run inpainting with ControlNet for better geometry preservation.

    Args:
        request: InpaintRequest

    Returns:
        Base64 encoded result image
    """
    if controlnet_pipeline is None or canny_detector is None:
        raise HTTPException(status_code=503, detail="ControlNet not loaded")

    try:
        # Decode images
        image_data = base64.b64decode(request.image)
        mask_data = base64.b64decode(request.mask)

        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        mask = Image.open(io.BytesIO(mask_data)).convert("L")

        if image.size != mask.size:
            mask = mask.resize(image.size, Image.LANCZOS)

        # Generate Canny edge map
        canny_image = canny_detector(image)

        # Generate
        generator = (
            torch.Generator(device=device).manual_seed(request.seed)
            if request.seed is not None
            else None
        )

        result = controlnet_pipeline(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            image=image,
            mask_image=mask,
            control_image=canny_image,
            strength=request.strength,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps,
            generator=generator,
        )

        result_image = result.images[0]

        # Encode result
        buffer = io.BytesIO()
        result_image.save(buffer, format="JPEG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"image": result_b64}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ControlNet inpainting failed: {str(e)}"
        )


@app.post("/multi-edit")
async def multi_edit(request: MultiEditRequest):
    """
    Run multiple edits sequentially.

    Args:
        request: MultiEditRequest with image and list of edits

    Returns:
        Base64 encoded final result image
    """
    if inpaint_pipeline is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        # Decode initial image
        image_data = base64.b64decode(request.image)
        current_image = Image.open(io.BytesIO(image_data)).convert("RGB")

        # Process each edit
        for edit in request.edits:
            # Build prompt
            target = edit.get("target_object", "")
            operation = edit.get("operation", "")
            params = edit.get("parameters", {})

            if operation == "recolor":
                color = params.get("color", "")
                prompt = f"{target} in {color} color, {request.room_type}, realistic, high quality"
            elif operation == "texture":
                material = params.get("material", "")
                prompt = f"{target} with {material} texture, {request.room_type}, realistic, high quality"
            elif operation == "lighting":
                style = params.get("style", "")
                prompt = f"{target} with {style} lighting, {request.room_type}, realistic, high quality"
            else:
                prompt = f"{target} in {request.room_type}, realistic, high quality"

            # Get mask (this should come from the edit plan)
            # For now, create a placeholder mask
            # In production, masks should be provided in the edit data
            mask = Image.new("L", current_image.size, 255)  # Full mask as placeholder

            # Run inpainting
            strength = params.get("strength", 0.8)
            result = inpaint_pipeline(
                prompt=prompt,
                negative_prompt="blurry, distorted, low quality",
                image=current_image,
                mask_image=mask,
                strength=strength,
                guidance_scale=7.5,
                num_inference_steps=50,
            )

            current_image = result.images[0]

        # Encode final result
        buffer = io.BytesIO()
        current_image.save(buffer, format="JPEG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"image": result_b64}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-edit failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
