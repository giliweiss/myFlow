"""Repository for Lesson data access."""

from app.repositories.base_repo import BaseRepository


class LessonRepository(BaseRepository):
    """Repository for managing lessons."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lessons")

    def get_by_id(self, lesson_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", lesson_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def list_summaries_by_group(self, group_id: str, limit: int = 50) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("id, group_id, title, status, scheduled_for, created_at, updated_at, lesson_reviews(id)")
            .eq("group_id", group_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []

    def list_by_group_and_status(self, group_id: str, status: str) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("group_id", group_id)
            .eq("status", status)
            .execute()
        )
        return result.data or []

    def create(self, group_id: str, lesson_data: dict) -> dict:
        row = {
            "group_id": group_id,
            "status": "draft",
            **lesson_data,
        }
        result = self.client.table(self.table_name).insert(row).execute()
        if not result.data:
            raise RuntimeError("Failed to create lesson")
        return result.data[0]

    def update(self, lesson_id: str, lesson_data: dict) -> dict:
        result = (
            self.client.table(self.table_name)
            .update(lesson_data)
            .eq("id", lesson_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to update lesson: {lesson_id}")
        return result.data[0]
