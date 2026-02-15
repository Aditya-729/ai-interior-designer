"""
Authentication endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth import create_magic_link, verify_magic_link
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/auth/request-link")
async def request_magic_link(
    email: str = Body(...),
    db: Session = Depends(get_db),
):
    """
    Request magic link for authentication.
    
    Returns:
        {"message": "Magic link sent", "token": "..."} (in dev mode)
    """
    try:
        token = create_magic_link(email, db)
        
        # In production, send email here
        # For now, return token in dev mode
        if settings.ENVIRONMENT == "development":
            return {
                "message": "Magic link created",
                "token": token,  # Only in dev!
                "link": f"{settings.FRONTEND_URL}/auth/verify?token={token}",
            }
        
        # In production, send email
        return {"message": "Magic link sent to your email"}
    except Exception as e:
        logger.error(f"Failed to create magic link: {e}")
        raise HTTPException(status_code=500, detail="Failed to create magic link")


@router.post("/auth/verify-link")
async def verify_magic_link_endpoint(
    token: str = Body(...),
    response: Response = None,
    db: Session = Depends(get_db),
):
    """
    Verify magic link token and create session.
    
    Returns:
        {"user_id": "...", "email": "..."}
    """
    try:
        user = verify_magic_link(token, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Set session cookie (production-ready)
        is_production = settings.PRODUCTION or settings.ENVIRONMENT == "production"
        response.set_cookie(
            key="session_token",
            value=user.id,
            httponly=True,
            secure=is_production,  # HTTPS required in production
            samesite="none" if is_production else "lax",  # None for cross-site in production
            max_age=86400 * 7,  # 7 days
            path="/",
        )

        return {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to verify magic link: {e}")
        raise HTTPException(status_code=500, detail="Failed to verify magic link")


@router.post("/auth/logout")
async def logout(response: Response):
    """Logout user by clearing session cookie."""
    response.delete_cookie("session_token")
    return {"message": "Logged out"}
