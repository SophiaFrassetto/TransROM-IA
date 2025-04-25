"""Configuration management for the TransROM-IA backend.

This module handles all configuration settings
for the application using pydantic-settings.

It loads configuration from environment variables
and provides type-safe access to all settings.
"""

from functools import lru_cache
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings management class.

    This class handles all configuration settings for the application, including:
    - API configuration
    - Database settings
    - Security settings
    - External service configurations
    - Feature flags

    All settings can be overridden using environment variables.

    Attributes:
        PROJECT_NAME (str): Name of the project
        VERSION (str): Current version of the API
        API_V1_STR (str): API version prefix
        SECRET_KEY (str): Secret key for JWT token generation
        ACCESS_TOKEN_EXPIRE_MINUTES (int): JWT token expiration time in minutes
        BACKEND_CORS_ORIGINS (List[AnyHttpUrl]): List of allowed CORS origins
        POSTGRES_SERVER (str): PostgreSQL server hostname
        POSTGRES_USER (str): PostgreSQL username
        POSTGRES_PASSWORD (str): PostgreSQL password
        POSTGRES_DB (str): PostgreSQL database name
        POSTGRES_PORT (int): PostgreSQL port number
        SQLALCHEMY_DATABASE_URI (Optional[PostgresDsn]): Complete database URI
        SMTP_TLS (bool): Whether to use TLS for email
        SMTP_PORT (Optional[int]): SMTP port number
        SMTP_HOST (Optional[str]): SMTP host
        SMTP_USER (Optional[str]): SMTP username
        SMTP_PASSWORD (Optional[str]): SMTP password
        EMAILS_FROM_EMAIL (Optional[EmailStr]): Sender email address
        EMAILS_FROM_NAME (Optional[str]): Sender name
        EMAIL_RESET_TOKEN_EXPIRE_HOURS (int): Password reset token expiration
        EMAIL_TEMPLATES_DIR (str): Directory containing email templates
        EMAILS_ENABLED (bool): Whether email functionality is enabled
        GOOGLE_CLIENT_ID (str): Google OAuth client ID
        GOOGLE_CLIENT_SECRET (str): Google OAuth client secret
        GOOGLE_REDIRECT_URI (str): Google OAuth redirect URI
        ENVIRONMENT (str): Current environment (development/staging/production)
        UPLOAD_DIR (str): Directory for storing uploaded files
        FRONTEND_URL (str): URL of the frontend application
        ALGORITHM (str): Algorithm used for JWT token generation
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # API Settings
    PROJECT_NAME: str = "TransROM-IA"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[AnyHttpUrl] | str:
        """Validate and process CORS origins configuration.

        Args:
            v: String or list of strings representing allowed origins

        Returns:
            List of validated HTTP URLs or the original string if validation fails

        Raises:
            ValueError: If the provided URLs are invalid
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        """Construct database URI from components.

        Args:
            v: Optional existing URI
            info: Validation context information

        Returns:
            Complete PostgreSQL connection URI

        Raises:
            ValueError: If required database settings are missing
        """
        if isinstance(v, str):
            return v

        data = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=data.get("POSTGRES_USER"),
            password=data.get("POSTGRES_PASSWORD"),
            host=data.get("POSTGRES_SERVER", ""),
            port=data.get("POSTGRES_PORT", 5432),
            path=f"{data.get('POSTGRES_DB') or ''}",
        )

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "app/email-templates"
    EMAILS_ENABLED: bool = False

    # OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:3000/auth/callback"

    # Application
    ENVIRONMENT: str = "development"
    UPLOAD_DIR: str = "uploads"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Cached settings instance

    Example:
        ```python
        settings = get_settings()
        database_url = settings.SQLALCHEMY_DATABASE_URI
        ```
    """
    return Settings()
