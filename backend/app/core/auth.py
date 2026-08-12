"""Authentication helpers for Supabase JWT verification."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

security = HTTPBearer(auto_error=False)


def is_dev_auth_bypass_enabled() -> bool:
    return settings.dev_auth_bypass and settings.environment == "development"


def get_dev_user() -> dict:
    return {
        "user_id": settings.dev_user_id,
        "email": "dev@local.test",
        "token": None,
    }


def _get_supabase_auth_client():
    from supabase import create_client

    return create_client(settings.supabase_url, settings.supabase_service_key)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """Verify a Supabase access token and return the authenticated user."""
    if is_dev_auth_bypass_enabled():
        return get_dev_user()

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        auth_response = _get_supabase_auth_client().auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if auth_response is None or auth_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = auth_response.user
    return {
        "user_id": user.id,
        "email": user.email,
        "token": token,
    }


def verify_instructor_ownership(user: dict, resource_instructor_id: str) -> bool:
    """Verify that the user owns the resource."""
    return user.get("user_id") == resource_instructor_id
