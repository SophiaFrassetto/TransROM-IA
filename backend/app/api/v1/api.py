"""API router configuration for v1 endpoints.

This module aggregates all API v1 endpoints into a single router.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, translations, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    translations.router, prefix="/translations", tags=["translations"]
)
