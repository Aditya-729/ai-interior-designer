"""
Transcription endpoints for voice input.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.whisper_service import whisper_service
from app.storage import storage

router = APIRouter()


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = None,
):
    """
    Transcribe audio to text using Whisper.

    Args:
        file: Audio file
        language: Optional language code (e.g., 'en')

    Returns:
        {
            "text": "transcribed text",
            "language": "en",
            "segments": [...]
        }
    """
    # Read audio file
    audio_data = await file.read()

    # Transcribe
    try:
        result = whisper_service.transcribe(audio_data, language=language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/transcribe-from-url")
async def transcribe_from_url(
    audio_url: str,
    language: str = None,
):
    """
    Transcribe audio from a stored URL.

    Args:
        audio_url: URL of stored audio file
        language: Optional language code

    Returns:
        Transcription result
    """
    # Download audio from storage (implement if needed)
    # For now, this is a placeholder
    raise HTTPException(
        status_code=501, detail="Transcription from URL not yet implemented"
    )
