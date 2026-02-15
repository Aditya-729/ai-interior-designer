"""
Usage statistics endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.usage_limiter import UsageLimiter
from app.middleware.auth import require_auth
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/usage")
async def get_usage(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Get current usage statistics for authenticated user.
    
    Returns:
        {
            "projects": {"current": 5, "limit": 10},
            "edits": {"today": 3, "limit": 50},
            "inference": {"today": 2, "limit": 20}
        }
    """
    try:
        user_id = await require_auth(request)
        limiter = UsageLimiter(db)
        stats = limiter.get_usage_stats(user_id)
        return stats
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get usage stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get usage stats")
