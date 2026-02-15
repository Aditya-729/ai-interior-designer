"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.base import init_db
from app.api.v1 import upload, transcription, scene, planner, design_knowledge, inference, projects, auth, usage, share, export, system
from app.services.websocket_manager import websocket_manager

load_dotenv()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on startup/shutdown."""
    # Startup
    init_db()
    init_gpu_queue(max_concurrent=settings.GPU_MAX_CONCURRENT)
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="AI Interior Designer API",
    description="Backend API for interior design AI platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - production ready
allowed_origins = []
if settings.FRONTEND_PUBLIC_URL:
    allowed_origins.append(settings.FRONTEND_PUBLIC_URL)
if settings.FRONTEND_URL:
    allowed_origins.extend(settings.FRONTEND_URL.split(","))
if not allowed_origins:
    allowed_origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(transcription.router, prefix="/api/v1", tags=["transcription"])
app.include_router(scene.router, prefix="/api/v1", tags=["scene"])
app.include_router(planner.router, prefix="/api/v1", tags=["planner"])
app.include_router(design_knowledge.router, prefix="/api/v1", tags=["design-knowledge"])
app.include_router(inference.router, prefix="/api/v1", tags=["inference"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(usage.router, prefix="/api/v1", tags=["usage"])
app.include_router(share.router, prefix="/api/v1", tags=["share"])
app.include_router(export.router, prefix="/api/v1", tags=["export"])
app.include_router(system.router, prefix="/api/v1", tags=["system"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Interior Designer API"}


@app.get("/health")
async def health():
    """Detailed health check."""
    from app.db.session import SessionLocal
    from app.services.inference_client import check_inference_service
    
    db_status = "unknown"
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    inference_status = await check_inference_service()
    
    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "inference_service": inference_status,
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
