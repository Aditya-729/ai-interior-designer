"""
System endpoints for deployment verification.
"""

from fastapi import APIRouter
from datetime import datetime
from app.db.session import SessionLocal
from app.services.inference_client import check_inference_service
from app.services.gpu_queue import gpu_queue
from app.core.config import settings
from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/system/health")
async def system_health():
    """Public system health endpoint for deployment verification."""
    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    # Database check
    db_status = "unknown"
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
        health_data["status"] = "degraded"
    
    health_data["database"] = db_status
    
    # Qdrant check
    qdrant_status = "unknown"
    try:
        qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        qdrant_client.get_collections()
        qdrant_status = "connected"
    except Exception as e:
        qdrant_status = f"disconnected: {str(e)}"
        health_data["status"] = "degraded"
    
    health_data["qdrant"] = qdrant_status
    
    # Inference service check
    inference_status = await check_inference_service()
    if inference_status != "connected":
        health_data["status"] = "degraded"
    health_data["inference_service"] = inference_status
    
    # GPU queue status
    if gpu_queue:
        queue_status = gpu_queue.get_queue_status()
        health_data["gpu_queue"] = queue_status
    else:
        health_data["gpu_queue"] = {"status": "not_initialized"}
    
    return health_data


@router.get("/system/ws-url")
async def get_ws_url():
    """Get WebSocket URL for frontend."""
    # Use public backend URL if available
    backend_url = settings.public_backend_url
    
    # Convert http/https to ws/wss
    if backend_url.startswith("https://"):
        ws_url = backend_url.replace("https://", "wss://")
    elif backend_url.startswith("http://"):
        ws_url = backend_url.replace("http://", "ws://")
    else:
        ws_url = f"wss://{backend_url}"
    
    return {
        "ws_url": f"{ws_url}/ws",
        "backend_url": backend_url,
    }
