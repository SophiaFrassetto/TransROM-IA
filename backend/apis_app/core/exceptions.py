"""Exception handling for the TransROM-IA backend.

This module defines custom exceptions and exception handlers for the application.
It provides a consistent way to handle and report errors across the application.
"""

from typing import Any, Dict, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .logging import get_logger

logger = get_logger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response model.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Optional additional error details
    """

    message: str
    error_code: str
    details: Optional[Dict[str, Any]] = None


class AppError(Exception):
    """Base exception for application-specific errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        status_code: HTTP status code
        details: Optional additional error details
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            status_code: HTTP status code (default: 400)
            details: Optional additional error details
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional additional error details
        """
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional additional error details
        """
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: str = "AUTHENTICATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional additional error details
        """
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class AuthorizationError(AppError):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str = "Not authorized",
        error_code: str = "AUTHORIZATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional additional error details
        """
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class DatabaseError(AppError):
    """Raised when a database operation fails."""

    def __init__(
        self,
        message: str = "Database error",
        error_code: str = "DATABASE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Optional additional error details
        """
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
        )


def setup_exception_handlers(app: FastAPI) -> None:
    """Configure exception handlers for the application.

    Args:
        app: FastAPI application instance

    Example:
        ```python
        from fastapi import FastAPI
        from app.core.exceptions import setup_exception_handlers

        app = FastAPI()
        setup_exception_handlers(app)
        ```
    """

    @app.exception_handler(AppError)
    async def app_exception_handler(
        request: Request, exc: AppError
    ) -> JSONResponse:
        """Handle application-specific exceptions.

        Args:
            request: FastAPI request instance
            exc: Exception instance

        Returns:
            JSONResponse: Standardized error response
        """
        logger.error(
            "Application error: %s - %s - %s",
            exc.error_code,
            exc.message,
            exc.details,
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_details": exc.details,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=exc.message,
                error_code=exc.error_code,
                details=exc.details,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unhandled exceptions.

        Args:
            request: FastAPI request instance
            exc: Exception instance

        Returns:
            JSONResponse: Standardized error response
        """
        logger.exception(
            "Unhandled error: %s",
            str(exc),
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Internal server error",
                error_code="INTERNAL_ERROR",
                details={"error": str(exc)} if app.debug else None,
            ).model_dump(),
        )
