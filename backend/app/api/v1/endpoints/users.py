"""User endpoints for TransROM-IA.

This module provides user-related endpoints, including user profile
management and user information retrieval.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.services.user import user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: Annotated[UserResponse, Depends(user_service.get_current_user)],
) -> UserResponse:
    """Get current authenticated user.

    Args:
        current_user: Current authenticated user from dependency

    Returns:
        UserResponse: Current user information
    """
    return current_user 