"""Repository for group member roster data access."""

from app.repositories.base_repo import BaseRepository


class GroupMemberRepository(BaseRepository):
    """Repository for managing group members."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "group_members")

    def list_by_group(self, group_id: str, include_inactive: bool = False) -> list[dict]:
        query = (
            self.client.table(self.table_name)
            .select("*")
            .eq("group_id", group_id)
            .order("name")
        )
        if not include_inactive:
            query = query.eq("is_active", True)

        result = query.execute()
        return (result.data if result else None) or []

    def list_active_by_group(self, group_id: str) -> list[dict]:
        return self.list_by_group(group_id, include_inactive=False)

    def get_by_id(self, member_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", member_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def get_by_id_for_group(self, group_id: str, member_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", member_id)
            .eq("group_id", group_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def create(self, group_id: str, name: str) -> dict:
        row = {
            "group_id": group_id,
            "name": name,
            "is_active": True,
        }
        result = self.client.table(self.table_name).insert(row).execute()
        if not result.data:
            raise RuntimeError("Failed to create group member")
        return result.data[0]

    def update(self, member_id: str, member_data: dict) -> dict:
        result = (
            self.client.table(self.table_name)
            .update(member_data)
            .eq("id", member_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to update group member: {member_id}")
        return result.data[0]
