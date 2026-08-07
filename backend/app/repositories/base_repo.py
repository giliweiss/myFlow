"""Base repository for Supabase data access."""


class BaseRepository:
    """Base class for repositories."""

    def __init__(self, supabase_client, table_name: str):
        self.client = supabase_client
        self.table_name = table_name

    async def get_by_id(self, id: str):
        """Get a record by ID."""
        # Stub: implement in Phase 1
        return None

    async def list_all(self, filters: dict = None):
        """List all records, optionally filtered."""
        # Stub: implement in Phase 1
        return []

    async def create(self, data: dict):
        """Create a new record."""
        # Stub: implement in Phase 1
        return data

    async def update(self, id: str, data: dict):
        """Update a record."""
        # Stub: implement in Phase 1
        return data

    async def delete(self, id: str):
        """Delete a record."""
        # Stub: implement in Phase 1
        pass
