"""Configuration settings for backend.

Reference: @backend/CLAUDE.md
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str

    # Better Auth Shared Secret (CRITICAL: Must match frontend)
    better_auth_secret: str

    # JWT Configuration
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # CORS
    cors_origins: str = "http://localhost:3000"

    # API
    api_port: int = 8000
    api_title: str = "Todo Evolution API"
    api_version: str = "0.2.0"
    api_description: str = "Phase II: Full-Stack Web Application"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins as list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
