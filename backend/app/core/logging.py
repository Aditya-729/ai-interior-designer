"""
Logging configuration.
"""

import logging
import sys
from app.core.config import settings


def setup_logging():
    """Configure application logging."""
    # In production, suppress debug logs
    if settings.PRODUCTION:
        log_level = logging.WARNING
    else:
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO if not settings.PRODUCTION else logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
