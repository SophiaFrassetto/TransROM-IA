from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apis_app.core.config import get_settings
from apis_app.database.session import get_async_session
from apis_app.models.user import User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def create_or_update_user(user_data: dict, db: AsyncSession):
    query = select(User).where(User.email == user_data["email"])
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user:
        # Update existing user
        for key, value in user_data.items():
            setattr(user, key, value)
    else:
        # Create new user
        if "password" in user_data:
            user_data["password"] = get_password_hash(user_data["password"])
        user = User(**user_data)
        db.add(user)

    await db.commit()
    await db.refresh(user)
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception from None
    except JWTError as err:
        raise credentials_exception from err

    query = select(User).where(User.id == int(user_id))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception from None
    return user


get_current_user_dependency = get_current_user(
    token=Depends(oauth2_scheme), db=Depends(get_async_session)
)
