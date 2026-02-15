"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    MINO_AI_API_KEY: str
    PERPLEXITY_API_KEY: str
    
    # Supabase (optional for now)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # Cloudflare R2 (S3-compatible)
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str = "ai-interior-designer"
    R2_ENDPOINT: str
    R2_PUBLIC_URL: Optional[str] = None  # Public URL prefix if using custom domain
    
    # Database (Supabase Postgres)
    SUPABASE_DB_HOST: Optional[str] = None
    SUPABASE_DB_PORT: int = 5432
    SUPABASE_DB_NAME: Optional[str] = None
    SUPABASE_DB_USER: Optional[str] = None
    SUPABASE_DB_PASSWORD: Optional[str] = None
    
    # Legacy Postgres (for local development)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "interior_designer"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    DATABASE_URL: Optional[str] = None
    
    # Vector Database
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # Inference Service
    INFERENCE_SERVICE_URL: str = "http://localhost:8001"
    INFERENCE_DEVICE: str = "cuda"
    INFERENCE_MODEL_PATH: str = "./models"
    
    # Application
    BACKEND_URL: str = "http://localhost:8000"
    PUBLIC_BACKEND_URL: Optional[str] = None  # Public URL for share links, etc.
    FRONTEND_URL: str = "http://localhost:3000"
    FRONTEND_PUBLIC_URL: Optional[str] = None  # Public frontend URL (Vercel)
    JWT_SECRET: str = "change-me-in-production"
    ENVIRONMENT: str = "development"
    PRODUCTION: bool = False
    
    # Whisper
    WHISPER_MODEL: str = "base"
    WHISPER_DEVICE: str = "cuda"
    
    # Stable Diffusion
    SD_MODEL_ID: str = "runwayml/stable-diffusion-inpainting"
    CONTROLNET_MODEL_ID: str = "lllyasviel/sd-controlnet-canny"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Demo mode (bypasses auth in development)
    DEMO_MODE: bool = False
    
    # GPU Queue settings
    GPU_MAX_CONCURRENT: int = 2
    GPU_QUEUE_MAX_SIZE: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate production settings
        if self.PRODUCTION and self.DEMO_MODE:
            import warnings
            warnings.warn("DEMO_MODE should be False when PRODUCTION is True")
    
    @property
    def database_url(self) -> str:
        """Get database URL (Supabase or local)."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # Use Supabase if configured
        if self.SUPABASE_DB_HOST and self.SUPABASE_DB_USER:
            return (
                f"postgresql://{self.SUPABASE_DB_USER}:{self.SUPABASE_DB_PASSWORD}"
                f"@{self.SUPABASE_DB_HOST}:{self.SUPABASE_DB_PORT}/{self.SUPABASE_DB_NAME}"
            )
        
        # Fallback to local Postgres
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def public_backend_url(self) -> str:
        """Get public backend URL."""
        return self.PUBLIC_BACKEND_URL or self.BACKEND_URL
    
    @property
    def public_frontend_url(self) -> str:
        """Get public frontend URL."""
        return self.FRONTEND_PUBLIC_URL or self.FRONTEND_URL


settings = Settings()
