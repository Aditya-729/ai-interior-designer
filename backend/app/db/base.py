"""
Database base configuration.
"""

from sqlalchemy.ext.declarative import declarative_base
from app.db.session import engine

Base = declarative_base()


def init_db():
    """Initialize database tables."""
    from app.db.models import user, project, image, version, history
    
    Base.metadata.create_all(bind=engine)
