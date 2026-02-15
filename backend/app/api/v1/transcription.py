"""
Transcription endpoints for voice input.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from app.services.whisper_service import whisper_service
from app.services.websocket_manager import websocket_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = None,
    client_id: str = None,
):
    """
    Transcribe audio to text using Whisper.
    
    Loads Whisper locally and transcribes audio.
    
    Args:
        file: Audio file
        language: Optional language code (e.g., 'en')
        client_id: Optional WebSocket client ID for progress updates
        
    Returns:
        {
            "text": "transcribed text",
            "language": "en",
            "segments": [...]
        }
    """
    try:
        # Send progress update if WebSocket connected
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "transcribing", "progress": 10, "message": "Loading audio..."}
            )
        
        # Read audio file
        audio_data = await file.read()
        
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "transcribing", "progress": 50, "message": "Transcribing with Whisper..."}
            )
        
        # Transcribe
        result = whisper_service.transcribe(audio_data, language=language)
        
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {
                    "status": "completed",
                    "progress": 100,
                    "message": "Transcription complete",
                    "text": result["text"]
                }
            )
        
        logger.info(f"Transcription complete: {len(result['text'])} characters")
        
        return result
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "error", "message": f"Transcription failed: {str(e)}"}
            )
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/transcribe-from-url")
async def transcribe_from_url(
    audio_url: str,
    language: str = None,
    client_id: str = None,
):
    """
    Transcribe audio from a stored URL.
    
    Downloads audio from storage and transcribes.
    """
    import httpx
    
    try:
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "transcribing", "progress": 10, "message": "Downloading audio..."}
            )
        
        # Download audio
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(audio_url)
            response.raise_for_status()
            audio_data = response.content
        
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "transcribing", "progress": 50, "message": "Transcribing..."}
            )
        
        # Transcribe
        result = whisper_service.transcribe(audio_data, language=language)
        
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {
                    "status": "completed",
                    "progress": 100,
                    "message": "Transcription complete",
                    "text": result["text"]
                }
            )
        
        return result
    except Exception as e:
        logger.error(f"Transcription from URL failed: {e}")
        if client_id:
            await websocket_manager.send_message(
                client_id,
                {"status": "error", "message": f"Transcription failed: {str(e)}"}
            )
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
