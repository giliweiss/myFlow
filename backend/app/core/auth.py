"""Authentication helpers for Supabase JWT verification."""

from fastapi import Depends, HTTPException, Header, status


async def get_current_user(authorization: str = Header(None)) -> dict:
    """
    Verify JWT token from Authorization header.

    Expected format: Bearer <token>
    In Phase 1, this will verify Supabase JWT tokens.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid scheme")
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    # Stub: in Phase 1, decode and verify JWT with Supabase public key
    return {"user_id": "stub-user-id", "token": token}


def verify_instructor_ownership(user: dict, resource_instructor_id: str) -> bool:
    """Verify that the user owns the resource."""
    # Stub: compare user_id with resource instructor_id
    return True
