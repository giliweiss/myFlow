"""Lesson generation orchestration service.

Coordinates:
- GroupRepository (load group context)
- LessonRepository (load history)
- ReviewRepository (load recent feedback)
- ExerciseRepository (load all exercises)
- ExerciseFilter (deterministic filtering)
- LLMService (generate plan)
- LessonValidator (validate result)
"""


class LessonGeneratorService:
    """Orchestrates the lesson generation flow."""

    def __init__(
        self,
        group_repo,
        lesson_repo,
        review_repo,
        exercise_repo,
        exercise_filter,
        llm_service,
        lesson_validator,
    ):
        self.group_repo = group_repo
        self.lesson_repo = lesson_repo
        self.review_repo = review_repo
        self.exercise_repo = exercise_repo
        self.exercise_filter = exercise_filter
        self.llm_service = llm_service
        self.lesson_validator = lesson_validator

    async def generate(self, group_id: str, params: dict) -> dict:
        """
        Generate a lesson for a group.

        Flow:
        1. Load group context
        2. Load recent lesson history (what was already done)
        3. Load recent reviews (instructor feedback)
        4. Get all exercises
        5. Filter exercises by group constraints + recency
        6. Call LLM to generate lesson plan
        7. Validate the result
        8. Save as draft
        9. Return lesson

        Args:
            group_id: The group to generate for
            params: Generation parameters (duration, intensity, goals, notes)

        Returns:
            Generated lesson dict with exercises
        """
        # Stub: to be implemented in Phase 1
        return {
            "lesson_id": "stub",
            "group_id": group_id,
            "status": "draft",
            "exercises": [],
            "message": "Lesson generation - to be implemented in Phase 1",
        }
