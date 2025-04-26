"""User service for TransROM-IA.

This module provides user-related business logic, including user management
and authentication operations.
"""

from datetime import UTC, datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.logging import get_logger
from app.database.session import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate, UserCreateGoogle, UserResponse, UserUpdate
from app.services.base import BaseService

settings = get_settings()
logger = get_logger(__name__)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


class UserService(BaseService[User, UserCreate, UserUpdate]):
    """Service for handling user-related operations.

    This service provides methods for user management and authentication,
    including password hashing, token generation, and user CRUD operations.
    """

    def __init__(self):
        """Initialize the user service."""
        super().__init__(User)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to compare against

        Returns:
            bool: Whether the password matches
        """
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password.

        Args:
            password: Plain text password

        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)

    def create_access_token(self, user_id: int) -> str:
        """Create a JWT access token.

        Args:
            user_id: User ID to include in the token

        Returns:
            str: JWT access token
        """
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {
            "exp": expire,
            "sub": str(user_id),
        }
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    async def authenticate(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[User]:
        """Authenticate a user with email and password.

        Args:
            db: Database session
            email: User's email
            password: User's password

        Returns:
            Optional[User]: Authenticated user or None

        Raises:
            AuthenticationError: If authentication fails
        """
        user = await self.get_by_email(db, email)
        if not user:
            raise AuthenticationError(message="Invalid email or password")
        if not user.password:
            raise AuthenticationError(message="User uses Google authentication")
        if not self.verify_password(password, user.password):
            raise AuthenticationError(message="Invalid email or password")
        return user

    async def authenticate_google(
        self, db: AsyncSession, user_data: UserCreateGoogle
    ) -> User:
        """Authenticate or create a user with Google OAuth data.

        Args:
            db: Database session
            user_data: User data from Google

        Returns:
            User: Authenticated or created user
        """
        user = await self.get_by_email(db, user_data.email)
        if user:
            # Update existing user with latest Google data
            update_data = UserUpdate(
                name=user_data.name,
                picture=user_data.picture,
            )
            return await self.update(db, db_obj=user, obj_in=update_data)

        # Create new user
        return await self.create(db, obj_in=user_data)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get a user by email.

        Args:
            db: Database session
            email: User's email

        Returns:
            Optional[User]: Found user or None
        """
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(
        self, db: AsyncSession, *, obj_in: UserCreate | UserCreateGoogle
    ) -> User:
        """Create a new user.

        This method overrides the base create method to handle password hashing
        and different creation schemas.

        Args:
            db: Database session
            obj_in: User creation data

        Returns:
            User: Created user
        """
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            picture=str(obj_in.picture) if obj_in.picture else None,
        )

        if isinstance(obj_in, UserCreate):
            db_obj.password = self.get_password_hash(obj_in.password)
        else:
            db_obj.google_id = obj_in.google_id

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """Update a user.

        This method overrides the base update method to handle password hashing.

        Args:
            db: Database session
            db_obj: Existing user object
            obj_in: User update data

        Returns:
            User: Updated user
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            update_data["password"] = self.get_password_hash(update_data["password"])
        if "picture" in update_data and update_data["picture"] is not None:
            update_data["picture"] = str(update_data["picture"])
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[AsyncSession, Depends(get_async_session)]
    ) -> UserResponse:
        """Get the current authenticated user.

        Args:
            token: JWT access token
            db: Database session

        Returns:
            UserResponse: Current user information

        Raises:
            HTTPException: If token is invalid or user not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError as err:
            raise credentials_exception from err

        query = select(self.model).where(self.model.id == int(user_id))
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        return UserResponse.model_validate(user)


# Create a global instance
user_service = UserService()
