from app.core.config import settings
from app.repositories.exercise_repo import ExerciseRepository


def get_supabase_client():
    """Get Supabase client."""
    from supabase import create_client

    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_exercise_repository() -> ExerciseRepository:
    return ExerciseRepository(get_supabase_client())
