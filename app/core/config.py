"""
This module defines the application settings using Pydantic's BaseSettings.
It loads configuration from environment variables and .env files,
providing a single source of truth for all configurable parameters in the app.
"""

import time

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    app_name: str = "Retail Inventory API"
    version: str = "0.0.0"
    debug: bool = False
    db_username: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    start_time: float = time.time()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


config = Settings()
