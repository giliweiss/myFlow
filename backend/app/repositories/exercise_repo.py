"""Repository for Exercise data access."""

from app.repositories.base_repo import BaseRepository


class ExerciseRepository(BaseRepository):
    """Repository for managing exercises."""

    def __init__(self, supabase_client):
        super().__init__(supabase_client, "exercises")

    def list_active(self) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("is_active", True)
            .order("name_en")
            .execute()
        )
        return result.data or []

    def get_by_id(self, exercise_id: str) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", exercise_id)
            .eq("is_active", True)
            .maybe_single()
            .execute()
        )
        return result.data

    def get_by_ids(self, exercise_ids: list[str]) -> list[dict]:
        if not exercise_ids:
            return []

        result = (
            self.client.table(self.table_name)
            .select("*")
            .in_("id", exercise_ids)
            .eq("is_active", True)
            .execute()
        )
        return result.data or []

    def get_restrictions_by_exercise_ids(self, exercise_ids: list[str]) -> dict[str, list[dict]]:
        if not exercise_ids:
            return {}

        result = (
            self.client.table("exercise_restrictions")
            .select("*")
            .in_("exercise_id", exercise_ids)
            .execute()
        )
        restrictions_by_exercise: dict[str, list[dict]] = {}
        for restriction in result.data or []:
            exercise_id = restriction["exercise_id"]
            restrictions_by_exercise.setdefault(exercise_id, []).append(restriction)
        return restrictions_by_exercise
