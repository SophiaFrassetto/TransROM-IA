"""Test configuration and fixtures for TransROM-IA.

This module provides test configuration and fixtures that can be
used across all test files.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.database.session import Base
from app.main import create_application

settings = get_settings()

# Use an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for testing.

    This fixture creates an event loop that can be used
    across all tests in a session.

    Yields:
        asyncio.AbstractEventLoop: Event loop instance
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine.

    This fixture creates a test database engine that can be used
    across all tests in a session.

    Yields:
        AsyncEngine: Test database engine
    """
    engine = create_async_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session.

    This fixture creates a test database session that can be used
    in individual tests.

    Args:
        test_engine: Test database engine

    Yields:
        AsyncSession: Test database session
    """
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def app(test_engine: AsyncEngine) -> FastAPI:
    """Create a test FastAPI application.

    This fixture creates a test FastAPI application that can be used
    in individual tests.

    Args:
        test_engine: Test database engine

    Returns:
        FastAPI: Test FastAPI application
    """
    app = create_application()
    app.state.engine = test_engine
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client.

    This fixture creates a test HTTP client that can be used
    to make requests in individual tests.

    Args:
        app: Test FastAPI application

    Yields:
        AsyncClient: Test HTTP client
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
def test_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Override settings for testing.

    This fixture overrides settings that should be different
    in the test environment.

    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    monkeypatch.setattr(settings, "ENVIRONMENT", "test")
    monkeypatch.setattr(settings, "SQLALCHEMY_DATABASE_URI", TEST_SQLALCHEMY_DATABASE_URL)
