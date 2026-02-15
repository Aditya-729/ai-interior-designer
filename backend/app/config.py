"""
Application configuration.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    mino_ai_api_key: str
    perplexity_api_key: str

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str

    # Cloudflare R2
    r2_account_id: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_bucket_name: str = "ai-interior-designer"
    r2_endpoint: str

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "interior_designer"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    # Vector Database
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # Inference Service
    inference_service_url: str = "http://localhost:8001"
    inference_device: str = "cuda"
    inference_model_path: str = "./models"

    # Application
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    jwt_secret: str
    environment: str = "development"

    # Whisper
    whisper_model: str = "base"
    whisper_device: str = "cuda"

    # Stable Diffusion
    sd_model_id: str = "runwayml/stable-diffusion-inpainting"
    controlnet_model_id: str = "lllyasviel/sd-controlnet-canny"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
