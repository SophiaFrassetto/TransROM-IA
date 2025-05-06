"""Authentication schemas for TransROM-IA.

This module provides Pydantic models for authentication-related data structures.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    """Schema for authentication token response.

    Attributes:
        access_token: The JWT access token
        token_type: The type of token (usually "bearer")
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    name: str | None = None
    picture: str | None = None


class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat() if dt else None
        }
    )


class RefreshTokenRequest(BaseModel):
    """Request schema for token refresh."""
    refresh_token: str
