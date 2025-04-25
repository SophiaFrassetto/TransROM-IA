"""Logging configuration for the TransROM-IA backend.

This module sets up logging for the application with proper formatting and handlers.
It supports different log levels based on the environment and can output to both
console and file handlers.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict

from .config import get_settings

settings = get_settings()

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging() -> None:
    """Configure logging for the application.

    This function sets up logging with the following features:
    - Console output for all environments
    - File output for non-development environments
    - Different log levels based on environment
    - Proper formatting with timestamps
    - Error tracking for critical issues

    Returns:
        None

    Example:
        ```python
        from app.core.logging import setup_logging

        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Application started")
        ```
    """
    # Determine log level based on environment
    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO

    # Base configuration
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
                "datefmt": LOG_DATE_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
                "level": log_level,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": log_level,
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
            "sqlalchemy": {
                "handlers": ["console"],
                "level": logging.WARNING,
                "propagate": False,
            },
        },
    }

    # Add file handler for non-development environments
    if settings.ENVIRONMENT != "development":
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "default",
            "level": log_level,
        }
        logging_config["loggers"][""]["handlers"].append("file")

    # Configure logging
    logging.config.dictConfig(logging_config)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured - Environment: %s, Level: %s",
        settings.ENVIRONMENT,
        logging.getLevelName(log_level),
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name.

    Args:
        name: The name of the logger, typically __name__

    Returns:
        logging.Logger: Configured logger instance

    Example:
        ```python
        from app.core.logging import get_logger

        logger = get_logger(__name__)
        logger.info("Processing started")
        ```
    """
    return logging.getLogger(name)
