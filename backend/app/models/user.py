"""User model for TransROM-IA.

This module defines the User model which represents user accounts
in the system, supporting both local and Google OAuth authentication.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class User(BaseModel):
    """User model representing application users.

    This model stores user information for both local and Google OAuth
    authenticated users. It includes basic user details, authentication
    information, and role flags.

    Attributes:
        email: User's email address (unique)
        google_id: Google OAuth ID (unique, optional)
        password: Hashed password (optional for Google OAuth users)
        name: User's full name
        picture: URL to user's profile picture
        is_active: Whether the user account is active
        is_superuser: Whether the user has superuser privileges
        translation_jobs: List of user's translation jobs
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(length=255),
        unique=True,
        index=True,
        nullable=False,
    )
    google_id: Mapped[str | None] = mapped_column(
        String(length=255),
        unique=True,
        index=True,
        nullable=True,
    )
    password: Mapped[str | None] = mapped_column(
        String(length=255),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )
    picture: Mapped[str | None] = mapped_column(
        String(length=1024),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships
    translation_jobs = relationship("TranslationJob", back_populates="user")
