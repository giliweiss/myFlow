"""Repository for Group data access."""

from app.repositories.base_repo import BaseRepository


class GroupRepository(BaseRepository):
    """Repository for managing groups."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "groups")

    def list_by_instructor(self, instructor_id: str) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("instructor_id", instructor_id)
            .eq("is_active", True)
            .order("weekday")
            .order("start_time")
            .execute()
        )
        return result.data or []

    def get_by_id(self, group_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", group_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def create(self, instructor_id: str, group_data: dict) -> dict:
        row = {
            "instructor_id": instructor_id,
            **group_data,
        }
        result = self.client.table(self.table_name).insert(row).execute()
        if not result.data:
            raise RuntimeError("Failed to create group")
        return result.data[0]

    def update(self, group_id: str, group_data: dict) -> dict:
        result = (
            self.client.table(self.table_name)
            .update(group_data)
            .eq("id", group_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to update group: {group_id}")
        return result.data[0]
