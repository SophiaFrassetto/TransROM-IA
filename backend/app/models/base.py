"""Base model class for TransROM-IA.

This module provides a base model class with common functionality
that all models should inherit from.
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class BaseModel(Base):
    """Base model class with common fields and functionality.

    This class provides common fields and functionality that should be
    present in all models, such as:
    - ID field
    - Creation timestamp
    - Update timestamp
    - JSON serialization
    - String representation

    Attributes:
        id: Primary key
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation of the model

        Example:
            ```python
            user = User(name="John")
            user_dict = user.to_dict()
            ```
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:
        """Get string representation of the model.

        Returns:
            str: String representation

        Example:
            ```python
            user = User(name="John")
            print(user)  # User(id=1, name="John")
            ```
        """
        values = ", ".join(f"{column.name}={getattr(self, column.name)!r}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}({values})"
