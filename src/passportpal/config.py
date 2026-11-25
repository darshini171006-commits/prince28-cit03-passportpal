"""All settings come from environment variables (or a local .env file)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "passportpal"
    app_env: Literal["local", "ci", "production"]

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    data_file: Path = Path("data/sample_records.json")

    # Database settings
    database_url: str = (
        "postgresql+psycopg://app:app@localhost:5433/app"  # pragma: allowlist secret
    )
    db_pool_size: int = 5
    db_max_overflow: int = 10


@lru_cache
def get_settings() -> Settings:
    """Build the settings once and reuse them."""
    return Settings()
