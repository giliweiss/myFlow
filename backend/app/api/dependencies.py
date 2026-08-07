from app.core.config import settings

# Shared dependencies (to be implemented in Phase 1)

def get_supabase_client():
    """Get Supabase client."""
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_service_key)
