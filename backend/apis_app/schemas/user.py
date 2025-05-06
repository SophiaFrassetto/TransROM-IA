"""User schemas for TransROM-IA.

This module defines Pydantic schemas for user-related operations,
including user creation, updates, and responses.
"""

from typing import Optional

from pydantic import EmailStr, HttpUrl

from apis_app.schemas.base import BaseAPISchema, BaseCreateSchema, BaseUpdateSchema


class UserBase(BaseAPISchema):
    """Base schema for user data.

    This schema defines the common attributes shared by all user-related schemas.

    Attributes:
        email: User's email address
        name: User's full name
        picture: URL to user's profile picture
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
    """

    email: EmailStr
    name: str
    picture: Optional[HttpUrl] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseCreateSchema):
    """Schema for creating a new user.

    This schema is used when creating a new user with local authentication.

    Attributes:
        email: User's email address
        password: User's password (will be hashed)
        name: User's full name
        picture: Optional URL to user's profile picture
    """

    email: EmailStr
    password: str
    name: str
    picture: Optional[HttpUrl] = None


class UserCreateGoogle(BaseCreateSchema):
    """Schema for creating a new user via Google OAuth.

    This schema is used when creating a new user with Google authentication.

    Attributes:
        email: User's email address
        google_id: Google OAuth ID
        name: User's full name
        picture: URL to user's profile picture
    """

    email: EmailStr
    google_id: str
    name: str
    picture: Optional[HttpUrl] = None


class UserUpdate(BaseUpdateSchema):
    """Schema for updating an existing user.

    This schema is used when updating user information. All fields
    are optional to allow partial updates.

    Attributes:
        name: User's full name
        picture: URL to user's profile picture
        is_active: Whether the user account is active
        password: New password (will be hashed)
    """

    name: Optional[str] = None
    picture: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user responses.

    This schema is used when returning user information in API responses.
    It includes all base user fields plus the ID and timestamps from BaseAPISchema.
    It explicitly excludes sensitive information like passwords.
    """

    pass


class UserInDB(UserBase):
    """Schema for internal user representation.

    This schema is used internally and includes sensitive information
    like hashed passwords. It should never be exposed via the API.

    Attributes:
        password: Hashed password
        google_id: Google OAuth ID
    """

    password: Optional[str] = None
    google_id: Optional[str] = None
