"""
SQLAlchemy database models.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


def generate_uuid():
    """Generate UUID string."""
    return str(uuid.uuid4())


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class Project(Base):
    """Project model."""
    __tablename__ = "projects"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    room_type = Column(String, nullable=True)  # living_room, bedroom, kitchen, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="projects")
    images = relationship("Image", back_populates="project", cascade="all, delete-orphan")
    versions = relationship("Version", back_populates="project", cascade="all, delete-orphan")
    edit_history = relationship("EditHistory", back_populates="project", cascade="all, delete-orphan")


class Image(Base):
    """Image model."""
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    original_url = Column(String, nullable=False)
    storage_key = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="images")


class Version(Base):
    """Version model for storing edited images."""
    __tablename__ = "versions"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    parent_version_id = Column(String, ForeignKey("versions.id"), nullable=True)
    image_url = Column(String, nullable=False)
    storage_key = Column(String, nullable=False)
    edit_plan = Column(JSON, nullable=True)  # Structured edit plan
    user_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="versions")
    parent_version = relationship("Version", remote_side=[id])


class EditHistory(Base):
    """Edit history model."""
    __tablename__ = "edit_history"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    version_id = Column(String, ForeignKey("versions.id"), nullable=True)
    user_prompt = Column(Text, nullable=False)
    edit_plan = Column(JSON, nullable=False)
    detected_objects = Column(JSON, nullable=True)  # Mino AI results
    design_knowledge = Column(JSON, nullable=True)  # Perplexity results
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="edit_history")


class UserPreferences(Base):
    """User preferences and style memory."""
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)
    preferred_colors = Column(JSON, nullable=True)  # ["warm beige", "navy blue", ...]
    preferred_materials = Column(JSON, nullable=True)  # ["marble", "wood", ...]
    preferred_styles = Column(JSON, nullable=True)  # ["modern", "minimalist", ...]
    room_type_preferences = Column(JSON, nullable=True)  # Per-room-type preferences
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")
