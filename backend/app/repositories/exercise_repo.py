"""Repository for Exercise data access."""

from app.repositories.base_repo import BaseRepository


class ExerciseRepository(BaseRepository):
    """Repository for managing exercises."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "exercises")

    async def list_all(self):
        """List all available exercises."""
        # Stub: query exercises WHERE is_active = true
        return []

    async def get_by_id(self, exercise_id: str):
        """Get a single exercise by ID."""
        # Stub: fetch from Supabase
        return None

    async def get_by_ids(self, exercise_ids: list):
        """Get multiple exercises by IDs."""
        # Stub: query WHERE id IN (...)
        return []
