"""Repository for lesson attendance records."""

from app.repositories.base_repo import BaseRepository


class LessonAttendanceRepository(BaseRepository):
    """Repository for managing lesson attendance."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lesson_attendance")

    def list_by_lesson(self, lesson_id: str) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*, group_members(id, name, is_active)")
            .eq("lesson_id", lesson_id)
            .execute()
        )
        return (result.data if result else None) or []

    def create_rows_for_members(
        self,
        lesson_id: str,
        group_member_ids: list[str],
    ) -> list[dict]:
        if not group_member_ids:
            return []

        rows = [
            {
                "lesson_id": lesson_id,
                "group_member_id": member_id,
                "registered": False,
                "attended": False,
            }
            for member_id in group_member_ids
        ]
        result = (
            self.client.table(self.table_name)
            .upsert(rows, on_conflict="lesson_id,group_member_id", ignore_duplicates=True)
            .execute()
        )
        return result.data or []

    def create_row_if_missing(self, lesson_id: str, group_member_id: str) -> dict | None:
        existing = (
            self.client.table(self.table_name)
            .select("*")
            .eq("lesson_id", lesson_id)
            .eq("group_member_id", group_member_id)
            .limit(1)
            .execute()
        )
        rows = (existing.data if existing else None) or []
        if rows:
            return rows[0]

        row = {
            "lesson_id": lesson_id,
            "group_member_id": group_member_id,
            "registered": False,
            "attended": False,
        }
        result = self.client.table(self.table_name).insert(row).execute()
        if not result.data:
            return None
        return result.data[0]

    def upsert_attendance_updates(
        self,
        lesson_id: str,
        updates: list[dict],
    ) -> list[dict]:
        if not updates:
            return self.list_by_lesson(lesson_id)

        rows = [
            {
                "lesson_id": lesson_id,
                "group_member_id": update["group_member_id"],
                "registered": update.get("registered", False),
                "attended": update.get("attended", False),
            }
            for update in updates
        ]
        result = (
            self.client.table(self.table_name)
            .upsert(rows, on_conflict="lesson_id,group_member_id")
            .execute()
        )
        return result.data or []
