"""
Authentication service for magic link auth.
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def generate_magic_link_token() -> str:
    """Generate a secure magic link token."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    """Hash token for storage."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_magic_link(user_email: str, db: Session) -> str:
    """
    Create magic link for user.
    
    Returns:
        Unhashed token to send to user
    """
    # Find or create user
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(email=user_email)
        db.add(user)
    
    # Generate token
    token = generate_magic_link_token()
    hashed_token = hash_token(token)
    
    # Store hashed token
    user.magic_link_token = hashed_token
    user.token_expiry = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    logger.info(f"Magic link created for user: {user_email}")
    return token


def verify_magic_link(token: str, db: Session) -> User | None:
    """
    Verify magic link token and return user.
    
    Returns:
        User if token is valid, None otherwise
    """
    hashed_token = hash_token(token)
    
    user = db.query(User).filter(
        User.magic_link_token == hashed_token,
        User.token_expiry > datetime.utcnow()
    ).first()
    
    if user:
        # Clear token after use
        user.magic_link_token = None
        user.token_expiry = None
        db.commit()
        logger.info(f"Magic link verified for user: {user.email}")
        return user
    
    return None


def get_current_user(session_token: str, db: Session) -> User | None:
    """
    Get current user from session token.
    
    In production, this would verify a JWT or session cookie.
    For now, we'll use a simple token lookup.
    """
    # Simple implementation - in production use proper session management
    user = db.query(User).filter(User.id == session_token).first()
    return user
