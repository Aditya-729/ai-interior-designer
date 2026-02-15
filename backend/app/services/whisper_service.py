"""
Whisper service for speech-to-text transcription.
"""

import whisper
from app.core.config import settings
import io
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class WhisperService:
    """Service for transcribing audio using Whisper."""

    def __init__(self):
        self.model_name = settings.WHISPER_MODEL
        self.device = settings.WHISPER_DEVICE
        self.model = None
        logger.info(f"Whisper service initialized: model={self.model_name}, device={self.device}")

    def _load_model(self):
        """Lazy load Whisper model."""
        if self.model is None:
            logger.info("Loading Whisper model...")
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info("Whisper model loaded")
        return self.model

    def transcribe(self, audio_data: bytes, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio to text.

        Args:
            audio_data: Audio file bytes
            language: Optional language code (e.g., 'en')

        Returns:
            {
                "text": "transcribed text",
                "language": "en",
                "segments": [...]
            }
        """
        try:
            model = self._load_model()

            # Load audio from bytes
            audio = whisper.load_audio(io.BytesIO(audio_data))

            # Transcribe
            result = model.transcribe(
                audio,
                language=language,
                task="transcribe",
                fp16=False if self.device == "cpu" else True,
            )

            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "segments": result.get("segments", []),
            }
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            raise


whisper_service = WhisperService()
