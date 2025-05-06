"""Main application module for TransROM-IA backend.

This module initializes and configures the FastAPI application with all its dependencies,
middleware, and routers. It serves as the entry point for the application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from apis_app.api.v1.api import api_router
from apis_app.core.config import get_settings
from apis_app.core.exceptions import setup_exception_handlers
from apis_app.core.logging import get_logger, setup_logging

# Initialize settings and logging
settings = get_settings()
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Handle application startup and shutdown events.

    Args:
        _: FastAPI application instance (unused)
    """
    # Startup
    logger.info(
        "Starting %s in %s mode",
        settings.PROJECT_NAME,
        settings.ENVIRONMENT,
    )
    yield
    # Shutdown
    logger.info("Shutting down %s", settings.PROJECT_NAME)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    This function:
    1. Creates the FastAPI instance
    2. Configures CORS middleware
    3. Sets up exception handlers
    4. Includes API routers
    5. Initializes database

    Returns:
        FastAPI: Configured FastAPI application instance

    Example:
        ```python
        app = create_application()
        ```
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-Assisted ROM Translation and Dubbing System",
        version=settings.VERSION,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
        + [settings.FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Add Gzip compression
    application.add_middleware(GZipMiddleware, minimum_size=1000)

    # Set up exception handlers
    setup_exception_handlers(application)

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()
