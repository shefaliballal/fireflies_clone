"""
Application configuration via environment variables and sensible defaults.

Centralizing settings here keeps secrets and deployment-specific values out of
business logic. Override any value with an environment variable (e.g.
DATABASE_URL) when deploying.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for the API and database layer."""

    app_name: str = "Fireflies Clone API"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./meetings.db"


def get_settings() -> Settings:
    """Build Settings from environment variables with fallbacks."""
    return Settings(
        app_name=os.getenv("APP_NAME", Settings.app_name),
        app_version=os.getenv("APP_VERSION", Settings.app_version),
        debug=os.getenv("DEBUG", "false").lower() in {"1", "true", "yes"},
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
    )
