"""
Usage limiter service for free-tier limits.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models.user import User, UsageStats, Project
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class UsageLimiter:
    """Service for checking and enforcing usage limits."""

    def __init__(self, db: Session):
        self.db = db

    def check_project_limit(self, user_id: str) -> tuple[bool, str]:
        """
        Check if user can create a new project.
        
        Returns:
            (allowed, message)
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"

        # Count existing projects
        project_count = self.db.query(Project).filter(
            Project.user_id == user_id
        ).count()

        if project_count >= user.max_projects:
            return False, f"Project limit reached ({user.max_projects} projects)"

        return True, "OK"

    def check_edit_limit(self, user_id: str) -> tuple[bool, str]:
        """
        Check if user can make another edit today.
        
        Returns:
            (allowed, message)
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"

        # Get today's stats
        today = date.today()
        stats = self.db.query(UsageStats).filter(
            UsageStats.user_id == user_id,
            func.date(UsageStats.date) == today
        ).first()

        if not stats:
            stats = UsageStats(user_id=user_id, date=datetime.utcnow(), edits_count=0)
            self.db.add(stats)
            self.db.commit()

        if stats.edits_count >= user.max_edits_per_day:
            return False, f"Daily edit limit reached ({user.max_edits_per_day} edits/day)"

        return True, "OK"

    def check_inference_limit(self, user_id: str) -> tuple[bool, str]:
        """
        Check if user can make another inference call today.
        
        Returns:
            (allowed, message)
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "User not found"

        # Get today's stats
        today = date.today()
        stats = self.db.query(UsageStats).filter(
            UsageStats.user_id == user_id,
            func.date(UsageStats.date) == today
        ).first()

        if not stats:
            stats = UsageStats(user_id=user_id, date=datetime.utcnow(), inference_count=0)
            self.db.add(stats)
            self.db.commit()

        if stats.inference_count >= user.max_inference_per_day:
            return False, f"Daily inference limit reached ({user.max_inference_per_day} calls/day)"

        return True, "OK"

    def increment_edit_count(self, user_id: str):
        """Increment edit count for user."""
        today = date.today()
        stats = self.db.query(UsageStats).filter(
            UsageStats.user_id == user_id,
            func.date(UsageStats.date) == today
        ).first()

        if not stats:
            stats = UsageStats(user_id=user_id, date=datetime.utcnow(), edits_count=0)
            self.db.add(stats)

        stats.edits_count += 1
        self.db.commit()
        logger.info(f"Incremented edit count for user {user_id}: {stats.edits_count}")

    def increment_inference_count(self, user_id: str):
        """Increment inference count for user."""
        today = date.today()
        stats = self.db.query(UsageStats).filter(
            UsageStats.user_id == user_id,
            func.date(UsageStats.date) == today
        ).first()

        if not stats:
            stats = UsageStats(user_id=user_id, date=datetime.utcnow(), inference_count=0)
            self.db.add(stats)

        stats.inference_count += 1
        self.db.commit()
        logger.info(f"Incremented inference count for user {user_id}: {stats.inference_count}")

    def get_usage_stats(self, user_id: str) -> dict:
        """
        Get current usage statistics for user.
        
        Returns:
            {
                "projects": {"current": 5, "limit": 10},
                "edits": {"today": 3, "limit": 50},
                "inference": {"today": 2, "limit": 20}
            }
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}

        # Count projects
        project_count = self.db.query(Project).filter(
            Project.user_id == user_id
        ).count()

        # Get today's stats
        today = date.today()
        stats = self.db.query(UsageStats).filter(
            UsageStats.user_id == user_id,
            func.date(UsageStats.date) == today
        ).first()

        if not stats:
            stats = UsageStats(user_id=user_id, date=datetime.utcnow(), edits_count=0, inference_count=0)
            self.db.add(stats)
            self.db.commit()

        return {
            "projects": {
                "current": project_count,
                "limit": user.max_projects,
            },
            "edits": {
                "today": stats.edits_count,
                "limit": user.max_edits_per_day,
            },
            "inference": {
                "today": stats.inference_count,
                "limit": user.max_inference_per_day,
            },
        }
