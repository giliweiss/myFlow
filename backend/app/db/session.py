"""Database session management for Supabase."""

from app.core.config import settings


def get_supabase_client():
    """Get Supabase client instance."""
    from supabase import create_client

    return create_client(
        settings.supabase_url,
        settings.supabase_service_key,
    )
