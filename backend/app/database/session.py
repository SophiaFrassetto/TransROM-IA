"""Database session management for TransROM-IA.

This module provides database session management utilities using SQLAlchemy's async engine
and session makers. It handles connection pooling and session lifecycle management.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All database models should inherit from this class to ensure
    they use the same metadata and configuration.
    """


def create_async_engine_instance() -> AsyncEngine:
    """Create an async SQLAlchemy engine instance.

    Returns:
        AsyncEngine: Configured async SQLAlchemy engine

    Example:
        ```python
        engine = create_async_engine_instance()
        ```
    """
    engine = create_async_engine(
        str(settings.SQLALCHEMY_DATABASE_URI),
        echo=settings.ENVIRONMENT == "development",
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    logger.info("Created async database engine")
    return engine


async_engine = create_async_engine_instance()

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get an async database session.

    This is a dependency that can be used in FastAPI endpoints
    to get a database session.

    Yields:
        AsyncSession: Async SQLAlchemy session

    Example:
        ```python
        from fastapi import Depends
        from app.database.session import get_async_session

        @app.get("/items")
        async def get_items(session: AsyncSession = Depends(get_async_session)):
            # Use session here
            pass
        ```
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.exception("Database session error: %s", str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_database() -> None:
    """Create all database tables.

    This function should be called during application startup
    to ensure all tables exist.

    Example:
        ```python
        await create_database()
        ```
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Created database tables")
