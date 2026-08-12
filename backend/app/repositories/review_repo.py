"""Repository for Lesson Review data access."""

from app.repositories.base_repo import BaseRepository


class ReviewRepository(BaseRepository):
    """Repository for managing lesson reviews."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lesson_reviews")

    def get_by_lesson_id(self, lesson_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("lesson_id", lesson_id)
            .limit(1)
            .execute()
        )
        rows = result.data or []
        return rows[0] if rows else None
    def upsert_for_lesson(self, lesson_id: str, review_data: dict) -> dict:
        row = {
            "lesson_id": lesson_id,
            **review_data,
        }
        result = (
            self.client.table(self.table_name)
            .upsert(row, on_conflict="lesson_id")
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to upsert review for lesson: {lesson_id}")
        return result.data[0]
