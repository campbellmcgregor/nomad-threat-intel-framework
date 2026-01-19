"""Application configuration."""

import os
import secrets
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "NOMAD Web Intake GUI"
    debug: bool = False

    # Security
    api_token: str = ""
    secret_key: str = secrets.token_urlsafe(32)

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/nomad_web.db"

    # Share links
    share_expiry_hours: int = 72
    share_token_length: int = 24

    # Paths
    data_dir: Path = Path("./data")
    reports_dir: Path = Path("./data/reports")

    # CORS
    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()

    # Ensure directories exist
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)

    return settings
