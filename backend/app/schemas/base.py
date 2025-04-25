"""Base schema classes for TransROM-IA.

This module provides base Pydantic schema classes that should be used
as base classes for all other schemas in the application.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema class with common configuration.

    This class provides common configuration that should be used
    by all schemas in the application.

    Attributes:
        model_config: Pydantic model configuration
    """

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model -> Pydantic model conversion
        json_encoders={datetime: lambda dt: dt.isoformat()},  # ISO format for dates
        validate_assignment=True,  # Validate attribute assignments
    )


class BaseAPISchema(BaseSchema):
    """Base schema for API responses.

    This class provides common fields that should be present
    in all API response schemas.

    Attributes:
        id: Record ID
        created_at: Creation timestamp
        updated_at: Last update timestamp (optional)
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class BaseCreateSchema(BaseSchema):
    """Base schema for create operations.

    This class should be used as a base for all create operation schemas.
    It ensures consistent handling of create operations across the application.
    """

    pass


class BaseUpdateSchema(BaseSchema):
    """Base schema for update operations.

    This class should be used as a base for all update operation schemas.
    It ensures consistent handling of update operations across the application.
    """

    pass


class PaginatedResponse(BaseSchema):
    """Schema for paginated responses.

    This class provides a standard format for paginated responses
    across the application.

    Attributes:
        items: List of items
        total: Total number of items
        page: Current page number
        size: Page size
        pages: Total number of pages
        has_next: Whether there is a next page
        has_prev: Whether there is a previous page
    """

    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    next_page: Optional[int] = None
    prev_page: Optional[int] = None

    def __init__(self, **data):
        """Initialize the paginated response.

        This method calculates pagination metadata based on
        the provided data.

        Args:
            **data: Pagination data
        """
        super().__init__(**data)
        self.pages = (self.total + self.size - 1) // self.size
        self.has_next = self.page < self.pages
        self.has_prev = self.page > 1
        self.next_page = self.page + 1 if self.has_next else None
        self.prev_page = self.page - 1 if self.has_prev else None
