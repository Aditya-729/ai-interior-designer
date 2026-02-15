"""
Database session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Build database URL with SSL for Supabase
db_url = settings.database_url
if settings.SUPABASE_DB_HOST and "sslmode" not in db_url:
    # Add SSL requirement for Supabase
    db_url += "?sslmode=require"

# Create engine
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    connect_args={"sslmode": "require"} if settings.SUPABASE_DB_HOST else {},
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
