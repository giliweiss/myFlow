"""Repository for Group data access."""

from app.repositories.base_repo import BaseRepository


class GroupRepository(BaseRepository):
    """Repository for managing groups."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "groups")

    async def get_by_id(self, group_id: str):
        """Get a group by ID (Phase 1: verify ownership via caller)."""
        # Stub: fetch from Supabase
        return None

    async def list_by_instructor(self, instructor_id: str):
        """List all groups for an instructor."""
        # Stub: query groups WHERE instructor_id = instructor_id
        return []

    async def create(self, instructor_id: str, group_data: dict):
        """Create a new group."""
        group_data["instructor_id"] = instructor_id
        # Stub: insert into Supabase
        return group_data

    async def update(self, group_id: str, data: dict):
        """Update a group."""
        # Stub: update in Supabase
        return data
