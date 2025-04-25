"""Authentication endpoints for TransROM-IA.

This module provides endpoints for user authentication, including local
authentication with email/password and Google OAuth authentication.
"""

from typing import Annotated, Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.logging import get_logger
from app.database.session import get_async_session
from app.schemas.auth import Token
from app.schemas.user import UserCreateGoogle
from app.services.user import user_service

settings = get_settings()
logger = get_logger(__name__)
router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Authenticate a user with email and password.

    Args:
        db: Database session
        form_data: Form containing email and password

    Returns:
        Token: Access token for the authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    try:
        user = await user_service.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        return Token(
            access_token=user_service.create_access_token(user.id),
            token_type="bearer",
        )
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.get("/google/url")
async def google_login_url() -> Dict[str, str]:
    """Get the Google OAuth2 login URL.

    Returns:
        Dict[str, str]: Dictionary containing the authorization URL
    """
    redirect_uri = f"{settings.FRONTEND_URL}/auth/callback"
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        "response_type=code&"
        f"redirect_uri={redirect_uri}&"
        "scope=email profile&"
        "access_type=offline"
    )
    logger.debug("Generated Google OAuth URL: %s", url)
    return {"url": url}


@router.post("/google/token", response_model=Token)
async def google_auth(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    code: Annotated[str, Query()],
) -> Token:
    """Handle Google OAuth2 callback and authenticate user.

    Args:
        db: Database session
        code: Authorization code from Google

    Returns:
        Token: Access token for the authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    redirect_uri = f"{settings.FRONTEND_URL}/auth/callback"
    logger.debug("Processing Google OAuth code for redirect_uri: %s", redirect_uri)

    try:
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
            logger.debug("Exchanging code for token at %s with data: %s", token_url, token_data)
            
            token_response = await client.post(token_url, data=token_data)
            token_json = token_response.json()
            
            if "error" in token_json:
                logger.error("Google OAuth token error: %s", token_json)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Google OAuth error: {token_json.get('error_description', token_json['error'])}",
                )

            # Get user info from Google
            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {token_json['access_token']}"}
            logger.debug("Fetching user info from %s", user_info_url)
            
            user_response = await client.get(user_info_url, headers=headers)
            user_data = user_response.json()
            
            if "error" in user_data:
                logger.error("Google user info error: %s", user_data)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to get user info: {user_data.get('error_description', user_data['error'])}",
                )

            logger.debug("Retrieved user data from Google: %s", {k: v for k, v in user_data.items() if k != "id"})

            # Create or update user
            google_user = UserCreateGoogle(
                email=user_data["email"],
                google_id=user_data["id"],
                name=user_data.get("name", user_data["email"].split("@")[0]),
                picture=user_data.get("picture"),
            )
            user = await user_service.authenticate_google(db, google_user)
            
            token = Token(
                access_token=user_service.create_access_token(user.id),
                token_type="bearer",
            )
            logger.info("Successfully authenticated Google user: %s", user.email)
            return token

    except httpx.RequestError as e:
        logger.error("Error communicating with Google: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error communicating with Google: {e!s}",
        ) from e
    except Exception as e:
        logger.error("Authentication failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {e!s}",
        ) from e
