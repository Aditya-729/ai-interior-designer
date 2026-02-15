"""
Export endpoints.
"""

from fastapi import APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.version import Version
from app.db.models.project import Project
from app.middleware.auth import require_auth
from app.services.storage import storage
from PIL import Image as PILImage, ImageDraw, ImageFont
import io
import httpx
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/projects/{project_id}/versions/{version_id}/export")
async def export_image(
    project_id: str,
    version_id: str,
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    Export edited image with watermark.
    
    Returns:
        Image file with watermark
    """
    # Require authentication
    user_id = await require_auth(request)
    
    # Verify project ownership
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get version
    version = db.query(Version).filter(
        Version.id == version_id,
        Version.project_id == project_id
    ).first()
    
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    try:
        # Download image
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(version.image_url)
            response.raise_for_status()
            image_data = response.content
        
        # Open image
        img = PILImage.open(io.BytesIO(image_data)).convert("RGB")
        
        # Add watermark
        watermarked_img = add_watermark(img)
        
        # Convert to bytes
        output = io.BytesIO()
        watermarked_img.save(output, format="JPEG", quality=95)
        output.seek(0)
        
        logger.info(f"Image exported: {version_id}")
        
        return Response(
            content=output.read(),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f'attachment; filename="interior-design-{version_id}.jpg"'
            }
        )
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


def add_watermark(image: PILImage.Image) -> PILImage.Image:
    """
    Add watermark to image.
    
    Args:
        image: PIL Image
        
    Returns:
        Watermarked image
    """
    # Create a copy
    watermarked = image.copy()
    
    # Get image dimensions
    width, height = watermarked.size
    
    # Create watermark text
    watermark_text = "AI Interior Designer"
    
    # Try to load a font, fallback to default
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Create drawing context
    draw = ImageDraw.Draw(watermarked)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Position watermark (bottom right with padding)
    x = width - text_width - 20
    y = height - text_height - 20
    
    # Draw semi-transparent background
    padding = 10
    draw.rectangle(
        [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
        fill=(0, 0, 0, 128)
    )
    
    # Draw text
    draw.text(
        (x, y),
        watermark_text,
        fill=(255, 255, 255, 200),
        font=font
    )
    
    return watermarked
