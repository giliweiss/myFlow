"""Repository for lesson exercise items."""

from app.repositories.base_repo import BaseRepository


class LessonExerciseRepository(BaseRepository):
    """Repository for managing lesson exercises."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "lesson_exercises")

    def list_by_lesson(self, lesson_id: str) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("lesson_id", lesson_id)
            .order("order_index")
            .execute()
        )
        return result.data or []

    def replace_for_lesson(self, lesson_id: str, exercises: list[dict]) -> list[dict]:
        self.client.table(self.table_name).delete().eq("lesson_id", lesson_id).execute()

        if not exercises:
            return []

        rows = [{"lesson_id": lesson_id, **exercise} for exercise in exercises]
        result = self.client.table(self.table_name).insert(rows).execute()
        return result.data or []

    def get_by_id_for_lesson(self, lesson_id: str, item_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", item_id)
            .eq("lesson_id", lesson_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def update_exercise_id(self, item_id: str, new_exercise_id: str) -> dict:
        result = (
            self.client.table(self.table_name)
            .update({"exercise_id": new_exercise_id})
            .eq("id", item_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to replace exercise item: {item_id}")
        return result.data[0]

    def update_completion_status(
        self,
        lesson_id: str,
        item_id: str,
        completion_status: str,
        actual_duration_seconds: int | None = None,
    ) -> dict:
        update_data = {"completion_status": completion_status}
        if actual_duration_seconds is not None:
            update_data["actual_duration_seconds"] = actual_duration_seconds

        result = (
            self.client.table(self.table_name)
            .update(update_data)
            .eq("id", item_id)
            .eq("lesson_id", lesson_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to update exercise completion: {item_id}")
        return result.data[0]
