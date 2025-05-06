"""Base CRUD service class for TransROM-IA.

This module provides a base service class with common CRUD operations
that all services should inherit from.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apis_app.core.exceptions import NotFoundError
from apis_app.core.logging import get_logger
from apis_app.models.base import BaseModel as DBBaseModel

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=DBBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations.

    This class provides common database operations that should be
    available in all services, such as:
    - Create
    - Read
    - Update
    - Delete
    - List

    Attributes:
        model: SQLAlchemy model class
    """

    def __init__(self, model: Type[ModelType]):
        """Initialize the service.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """Get a single record by ID.

        Args:
            db: Database session
            obj_id: Record ID

        Returns:
            Optional[ModelType]: Found record

        Example:
            ```python
            user = await service.get(db, 1)
            ```
        """
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_or_404(self, db: AsyncSession, obj_id: int) -> ModelType:
        """Get a single record by ID or raise 404.

        Args:
            db: Database session
            obj_id: Record ID

        Returns:
            ModelType: Found record

        Raises:
            NotFoundError: If record is not found

        Example:
            ```python
            try:
                user = await service.get_or_404(db, 1)
            except NotFoundError:
                # Handle not found
                pass
            ```
        """
        obj = await self.get(db, obj_id)
        if not obj:
            raise NotFoundError(
                message=f"{self.model.__name__} with id {obj_id} not found"
            )
        return obj

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List[ModelType]: List of found records

        Example:
            ```python
            users = await service.get_multi(db, skip=0, limit=10)
            ```
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record.

        Args:
            db: Database session
            obj_in: Create schema instance

        Returns:
            ModelType: Created record

        Example:
            ```python
            user = await service.create(db, obj_in=user_create)
            ```
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> ModelType:
        """Update a record.

        Args:
            db: Database session
            db_obj: Existing database object
            obj_in: Update data

        Returns:
            ModelType: Updated record

        Example:
            ```python
            user = await service.update(db, db_obj=user, obj_in=user_update)
            ```
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = (
            obj_in
            if isinstance(obj_in, dict)
            else obj_in.model_dump(exclude_unset=True)
        )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, obj_id: int) -> ModelType:
        """Delete a record.

        Args:
            db: Database session
            obj_id: Record ID

        Returns:
            ModelType: Deleted record

        Raises:
            NotFoundError: If record is not found

        Example:
            ```python
            deleted_user = await service.delete(db, id=1)
            ```
        """
        obj = await self.get_or_404(db, obj_id)
        await db.delete(obj)
        await db.commit()
        return obj
