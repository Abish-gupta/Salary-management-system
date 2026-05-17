"""Application configuration.

Uses pydantic-settings for type-safe environment variable loading.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        database_url: SQLite connection string. Defaults to a local file.
        app_name: Application name used in logs and API metadata.
        debug: Enable debug mode. Never True in production.
    """

    database_url: str = "sqlite:///./salary_management.db"
    app_name: str = "Salary Management API"
    debug: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    """Factory function for settings. Enables easy overriding in tests."""
    return Settings()
