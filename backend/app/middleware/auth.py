"""
Authentication middleware.
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth import get_current_user
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def get_current_user_id(request: Request) -> Optional[str]:
    """
    Get current user ID from request.
    
    Supports:
    - DEMO_MODE (bypasses auth)
    - Session cookie
    - Authorization header
    """
    # Demo mode bypass (only in development, never in production)
    if settings.ENVIRONMENT == "development" and settings.DEMO_MODE and not settings.PRODUCTION:
        # Return demo user ID
        return "demo-user-id"

    # Try session cookie
    session_token = request.cookies.get("session_token")
    if session_token:
        db = SessionLocal()
        try:
            user = get_current_user(session_token, db)
            if user:
                return user.id
        finally:
            db.close()

    # Try Authorization header
    credentials: HTTPAuthorizationCredentials = await security(request)
    if credentials:
        db = SessionLocal()
        try:
            user = get_current_user(credentials.credentials, db)
            if user:
                return user.id
        finally:
            db.close()

    return None


async def require_auth(request: Request) -> str:
    """
    Require authentication and return user ID.
    
    Raises:
        HTTPException if not authenticated
    """
    user_id = await get_current_user_id(request)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_id
