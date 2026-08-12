"""Repository for instructor profile data access."""

from app.repositories.base_repo import BaseRepository


class InstructorProfileRepository(BaseRepository):
    """Repository for managing instructor profiles."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "instructor_profiles")

    def get_by_id(self, instructor_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", instructor_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def upsert(self, instructor_id: str, display_name: str) -> dict:
        row = {
            "id": instructor_id,
            "display_name": display_name,
        }
        result = (
            self.client.table(self.table_name)
            .upsert(row, on_conflict="id")
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to upsert instructor profile: {instructor_id}")
        return result.data[0]
