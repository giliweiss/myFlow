"""Repository for instructor-owned custom exercises."""

from app.repositories.base_repo import BaseRepository


class InstructorExerciseRepository(BaseRepository):
    def __init__(self, supabase_client):
        super().__init__(supabase_client, "instructor_exercises")

    def list_active_by_instructor(self, instructor_id: str) -> list[dict]:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("instructor_id", instructor_id)
            .eq("is_archived", False)
            .order("name_he")
            .execute()
        )
        return result.data or []

    def get_by_id_for_instructor(
        self,
        exercise_id: str,
        instructor_id: str,
    ) -> dict | None:
        result = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", exercise_id)
            .eq("instructor_id", instructor_id)
            .maybe_single()
            .execute()
        )
        return result.data

    def create(self, instructor_id: str, exercise_data: dict) -> dict:
        row = {
            "instructor_id": instructor_id,
            **exercise_data,
        }
        result = self.client.table(self.table_name).insert(row).execute()
        if not result.data:
            raise RuntimeError("Failed to create instructor exercise")
        return result.data[0]

    def update(
        self,
        exercise_id: str,
        instructor_id: str,
        exercise_data: dict,
    ) -> dict:
        result = (
            self.client.table(self.table_name)
            .update(exercise_data)
            .eq("id", exercise_id)
            .eq("instructor_id", instructor_id)
            .execute()
        )
        if not result.data:
            raise RuntimeError(f"Failed to update instructor exercise: {exercise_id}")
        return result.data[0]

    def archive(self, exercise_id: str, instructor_id: str) -> dict:
        return self.update(
            exercise_id,
            instructor_id,
            {"is_archived": True},
        )
