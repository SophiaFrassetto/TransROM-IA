"""Base router class for TransROM-IA.

This module provides a base router class with common functionality
that all routers should inherit from.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.schemas.base import (
    BaseAPISchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    PaginatedResponse,
)
from app.services.base import BaseService

# Module-level dependency
db_dependency = Depends(get_async_session)

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseAPISchema)


class RouterConfig(BaseAPISchema):
    """Configuration for router initialization.

    Attributes:
        service: Service class
        get_schema: Schema for get operations
        prefix: Router prefix
        tags: Router tags
        create_schema: Optional schema for create operations
        update_schema: Optional schema for update operations
    """
    service: Type[BaseService]
    get_schema: Type[GetSchemaType]
    prefix: str
    tags: List[str]
    create_schema: Optional[Type[CreateSchemaType]] = None
    update_schema: Optional[Type[UpdateSchemaType]] = None


class BaseRouter(Generic[ModelType, CreateSchemaType, UpdateSchemaType, GetSchemaType]):
    """Base router class with common CRUD endpoints.

    This class provides common CRUD endpoints that should be
    available in all routers, such as:
    - Create
    - Read
    - Update
    - Delete
    - List

    Attributes:
        router: FastAPI router instance
        service: Service class instance
        get_schema: Schema for get operations
        prefix: Router prefix
        tags: Router tags
    """

    def __init__(
        self,
        *,
        config: RouterConfig,
    ):
        """Initialize the router.

        Args:
            config: Router configuration
        """
        self.router = APIRouter(prefix=config.prefix, tags=config.tags)
        self.service = config.service
        self.get_schema = config.get_schema
        self.create_schema = config.create_schema
        self.update_schema = config.update_schema

        # Register routes based on available schemas
        self._register_get_routes()
        if config.create_schema:
            self._register_create_routes()
        if config.update_schema:
            self._register_update_routes()

    def _register_get_routes(self) -> None:
        """Register get routes.

        This method registers the following routes:
        - GET /{obj_id} - Get single item
        - GET / - Get multiple items with pagination
        """

        @self.router.get("/{obj_id}", response_model=self.get_schema)
        async def get_by_id(
            obj_id: int,
            db: AsyncSession = db_dependency,
        ) -> Any:
            """Get a single item by ID.

            Args:
                obj_id: Item ID
                db: Database session

            Returns:
                Any: Found item
            """
            return await self.service.get_or_404(db, obj_id)

        @self.router.get("/", response_model=PaginatedResponse)
        async def get_multi(
            db: AsyncSession = db_dependency,
            page: int = Query(1, ge=1, description="Page number"),
            size: int = Query(10, ge=1, le=100, description="Page size"),
        ) -> Any:
            """Get multiple items with pagination.

            Args:
                db: Database session
                page: Page number
                size: Page size

            Returns:
                Any: Paginated response with items
            """
            skip = (page - 1) * size
            items = await self.service.get_multi(db, skip=skip, limit=size)
            return {
                "items": items,
                "total": len(items),  # TODO: Add proper count query
                "page": page,
                "size": size,
            }

    def _register_create_routes(self) -> None:
        """Register create routes.

        This method registers the following routes:
        - POST / - Create new item
        """
        if not self.create_schema:
            return

        @self.router.post("/", response_model=self.get_schema)
        async def create(
            *,
            db: AsyncSession = db_dependency,
            obj_in: self.create_schema,
        ) -> Any:
            """Create a new item.

            Args:
                db: Database session
                obj_in: Create schema instance

            Returns:
                Any: Created item
            """
            return await self.service.create(db, obj_in=obj_in)

    def _register_update_routes(self) -> None:
        """Register update routes.

        This method registers the following routes:
        - PUT /{obj_id} - Update item
        - DELETE /{obj_id} - Delete item
        """
        if not self.update_schema:
            return

        @self.router.put("/{obj_id}", response_model=self.get_schema)
        async def update(
            *,
            db: AsyncSession = db_dependency,
            obj_id: int,
            obj_in: self.update_schema,
        ) -> Any:
            """Update an item.

            Args:
                db: Database session
                obj_id: Item ID
                obj_in: Update schema instance

            Returns:
                Any: Updated item
            """
            db_obj = await self.service.get_or_404(db, obj_id)
            return await self.service.update(db, db_obj=db_obj, obj_in=obj_in)

        @self.router.delete("/{obj_id}", response_model=self.get_schema)
        async def delete(
            *,
            db: AsyncSession = db_dependency,
            obj_id: int,
        ) -> Any:
            """Delete an item.

            Args:
                db: Database session
                obj_id: Item ID

            Returns:
                Any: Deleted item
            """
            return await self.service.delete(db, id=obj_id)
