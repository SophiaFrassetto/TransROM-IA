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


class UserCreate(BaseModel):
    """Schema for user registration data.

    Attributes:
        email: User's email address
        password: User's password
        full_name: User's full name
    """

    email: EmailStr
    password: str
    full_name: str


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


class LoginData(BaseModel):
    """Schema for login request data.

    Attributes:
        email: User's email address
        password: User's password
    """

    email: EmailStr
    password: str
