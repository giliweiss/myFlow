import json

from fastapi import HTTPException, status
from openai import OpenAI

from app.schemas.lesson_generation import GenerateLessonRequest, resolve_intention
from app.schemas.llm_lesson_plan import LLMClarificationOutput, LLMPlanningOutput
from app.services.clarification_rules import ForcedClarification
from app.services.lesson_planning_context import LessonPlanningContext

PLANNING_SYSTEM_INSTRUCTIONS = """
You are a Pilates lesson planning assistant for group instructors.

Rules:
- Return status "ready" when you can plan a purposeful lesson from the context.
- Return status "needs_clarification" with 1-2 questions only when intent is professionally ambiguous after deterministic checks passed.
- Build warmup, main, and cooldown sections using ONLY exercise IDs from the preparation catalog.
- Never invent exercises or IDs that are not in the preparation catalog.
- Respect the group's level, equipment, and considerations.
- Match the requested lesson duration with sensible planned_duration_seconds per exercise.
- Use unique sequential order_index values starting at 0 across the full lesson.
- When a target exercise is provided, explain progression logic in guidance even if the target is above group level.
- Include alternatives only when they add clear value and must also come from the preparation catalog.
- Provide professional guidance: lesson strategy, structure rationale, progression logic, section notes, and per-exercise teaching cues.
""".strip()

CLARIFICATION_SYSTEM_INSTRUCTIONS = """
You are a Pilates lesson planning assistant.

The backend has determined that clarification is required before planning can continue.
Write 1-2 concise, professional questions for the instructor.
Use the provided question_id values exactly as given.
Do not plan a lesson in this step.
""".strip()


class OpenAIService:
    def __init__(self, api_key: str, model: str, client: OpenAI | None = None):
        self._api_key = api_key
        self._model = model
        self._client = client

    def formulate_clarification_questions(
        self,
        group: dict,
        request: GenerateLessonRequest,
        forced_clarifications: list[ForcedClarification],
    ) -> LLMClarificationOutput:
        client = self._get_client()

        user_input = {
            "group": self._build_group_payload(group),
            "intention": resolve_intention(request),
            "notes": request.notes,
            "forced_clarifications": [
                {
                    "question_id": clarification.question_id,
                    "topic": clarification.topic,
                    "why_needed": clarification.why_needed,
                    "candidates": clarification.candidates,
                }
                for clarification in forced_clarifications
            ],
        }

        try:
            response = client.responses.parse(
                model=self._model,
                instructions=CLARIFICATION_SYSTEM_INSTRUCTIONS,
                input=json.dumps(user_input, ensure_ascii=False),
                text_format=LLMClarificationOutput,
            )
        except Exception as error:
            return self._fallback_clarification_output(forced_clarifications, error)

        output = response.output_parsed
        if output is None or not output.clarification_questions:
            return self._fallback_clarification_output(forced_clarifications)

        return output

    def generate_lesson_plan(
        self,
        group: dict,
        request: GenerateLessonRequest,
        planning_context: LessonPlanningContext,
    ) -> LLMPlanningOutput:
        client = self._get_client()

        user_input = {
            "group": self._build_group_payload(group),
            "lesson_request": {
                "intention": planning_context.intention,
                "planned_duration_minutes": request.planned_duration_minutes,
                "notes": request.notes,
                "clarification_answers": [
                    {"question_id": answer.question_id, "answer": answer.answer}
                    for answer in request.clarification_answers
                ],
            },
            "target_exercise": self._build_target_exercise_payload(planning_context),
            "preparation_catalog": self._build_exercise_catalog_payload(planning_context.preparation_catalog),
            "target_relations": planning_context.target_relations,
        }

        try:
            response = client.responses.parse(
                model=self._model,
                instructions=PLANNING_SYSTEM_INSTRUCTIONS,
                input=json.dumps(user_input, ensure_ascii=False),
                text_format=LLMPlanningOutput,
            )
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI lesson generation failed: {error}",
            ) from error

        plan = response.output_parsed
        if plan is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OpenAI returned an empty lesson plan",
            )

        return plan

    def _get_client(self) -> OpenAI:
        if self._client is not None:
            return self._client

        if not self._api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI API key is not configured",
            )

        return OpenAI(api_key=self._api_key)

    def _build_group_payload(self, group: dict) -> dict:
        return {
            "name": group.get("name"),
            "level": group.get("level"),
            "available_equipment": group.get("available_equipment") or [],
            "group_considerations": group.get("group_considerations") or [],
            "typical_duration_minutes": group.get("typical_duration_minutes"),
        }

    def _build_target_exercise_payload(self, planning_context: LessonPlanningContext) -> dict | None:
        if planning_context.target_exercise is None:
            return None

        exercise = planning_context.target_exercise
        return {
            "id": exercise["id"],
            "name_en": exercise.get("name_en"),
            "name_he": exercise.get("name_he"),
            "difficulty_level": exercise.get("difficulty_level"),
            "above_group_level": planning_context.target_above_group_level,
        }

    def _build_exercise_catalog_payload(self, exercises: list[dict]) -> list[dict]:
        return [
            {
                "id": exercise["id"],
                "name_en": exercise["name_en"],
                "name_he": exercise.get("name_he"),
                "difficulty_level": exercise["difficulty_level"],
                "body_focus": exercise.get("body_focus") or [],
                "position": exercise.get("position"),
                "intensity": exercise.get("intensity"),
                "min_duration_seconds": exercise.get("min_duration_seconds"),
                "max_duration_seconds": exercise.get("max_duration_seconds"),
                "min_reps": exercise.get("min_reps"),
                "max_reps": exercise.get("max_reps"),
                "possible_equipment": exercise.get("possible_equipment") or [],
            }
            for exercise in exercises
        ]

    def _fallback_clarification_output(
        self,
        forced_clarifications: list[ForcedClarification],
        error: Exception | None = None,
    ) -> LLMClarificationOutput:
        from app.schemas.llm_lesson_plan import LLMClarificationQuestion

        questions = [
            LLMClarificationQuestion(
                question_id=clarification.question_id,
                prompt=clarification.topic,
                why_needed=clarification.why_needed,
            )
            for clarification in forced_clarifications[:2]
        ]
        if error is not None and not questions:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI clarification generation failed: {error}",
            ) from error
        return LLMClarificationOutput(clarification_questions=questions)
