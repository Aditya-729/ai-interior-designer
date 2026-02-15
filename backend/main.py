"""
Main FastAPI application for AI Interior Designer backend.
"""

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import init_db
from app.routers import (
    upload,
    transcribe,
    analyze,
    plan,
    knowledge,
    inference,
    projects,
    history,
    preferences,
)
from app.websocket import websocket_manager

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on startup/shutdown."""
    # Startup
    init_db()
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="AI Interior Designer API",
    description="Backend API for interior design AI platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("FRONTEND_URL", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(transcribe.router, prefix="/api", tags=["transcribe"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(plan.router, prefix="/api", tags=["plan"])
app.include_router(knowledge.router, prefix="/api", tags=["knowledge"])
app.include_router(inference.router, prefix="/api", tags=["inference"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(preferences.router, prefix="/api", tags=["preferences"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Interior Designer API"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual health checks
        "inference_service": "connected",
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(client_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
