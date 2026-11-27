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

    # Application settings
    app_name: str = "passportpal"
    app_env: Literal["local", "ci", "production"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # Database settings
    database_url: str = "postgresql+psycopg://app:app@localhost:5433/app"
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # LLM gateway
    gemini_api_key: str = ""
    groq_api_key: str = ""
    llm_primary_model: str = "gemini-4-hydrogen"
    llm_fallback_model: str = "openai/gpt-oss-20b"
    llm_primary_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    llm_fallback_base_url: str = "https://api.groq.com/openai/v1"
    llm_timeout_seconds: float = 30.0
    usd_inr: float = 95.0
    prompts_dir: Path = Path("prompts")


@lru_cache
def get_settings() -> Settings:
    """Build the settings once and reuse them."""
    return Settings()
