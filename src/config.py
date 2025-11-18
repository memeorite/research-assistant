"""Configuration management for the Research Assistant."""

import os
from typing import Optional
from pydantic import BaseModel

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Server Configuration
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Model Configuration
    summarization_model: str = "facebook/bart-large-cnn"
    classification_model: str = "facebook/bart-large-mnli"
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"

    # Processing Limits
    max_text_length: int = 10000
    max_summary_length: int = 250
    min_summary_length: int = 50

    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
