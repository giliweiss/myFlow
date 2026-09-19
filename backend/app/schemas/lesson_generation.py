from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field


class ClarificationAnswer(BaseModel):
    question_id: str
    answer: str = Field(min_length=1)


class GenerateLessonRequest(BaseModel):
    intention: str | None = None
    planned_duration_minutes: int = Field(default=60, gt=0)
    notes: str | None = None
    clarification_answers: list[ClarificationAnswer] = Field(default_factory=list)
    primary_goal: str | None = None
    secondary_goals: list[str] = Field(default_factory=list)


class ClarificationQuestion(BaseModel):
    question_id: str
    prompt: str
    why_needed: str | None = None


class GeneratedExerciseAlternative(BaseModel):
    exercise_id: UUID
    relation_type: Literal["alternative", "regression", "progression"] = "alternative"
    reason: str | None = None


class GeneratedLessonExercise(BaseModel):
    exercise_id: UUID
    order_index: int = Field(ge=0)
    section: Literal["warmup", "main", "cooldown"]
    planned_duration_seconds: int | None = Field(default=None, gt=0)
    sets: int | None = Field(default=None, gt=0)
    reps: int | None = Field(default=None, gt=0)
    selected_modification: str | None = None
    instructor_notes: str | None = None
    alternatives: list[GeneratedExerciseAlternative] = Field(default_factory=list)


class GeneratedExerciseGuidance(BaseModel):
    exercise_id: UUID
    why_chosen: str | None = None
    progression_role: str | None = None
    teaching_cues: list[str] = Field(default_factory=list)
    creative_variations: list[str] = Field(default_factory=list)


class GeneratedLessonGuidance(BaseModel):
    lesson_strategy: str | None = None
    structure_rationale: str | None = None
    progression_logic: str | None = None
    section_notes: dict[str, str] = Field(default_factory=dict)
    exercise_guidance: list[GeneratedExerciseGuidance] = Field(default_factory=list)


class GenerateLessonClarificationResponse(BaseModel):
    status: Literal["needs_clarification"] = "needs_clarification"
    group_id: UUID
    clarification_questions: list[ClarificationQuestion] = Field(min_length=1, max_length=2)


class GenerateLessonReadyResponse(BaseModel):
    status: Literal["ready"] = "ready"
    group_id: UUID
    title: str
    primary_goal: str
    secondary_goals: list[str] = Field(default_factory=list)
    planned_duration_minutes: int
    instructor_notes: str | None = None
    lesson_exercises: list[GeneratedLessonExercise] = Field(default_factory=list)
    guidance: GeneratedLessonGuidance


GenerateLessonResponse = Annotated[
    Union[GenerateLessonClarificationResponse, GenerateLessonReadyResponse],
    Field(discriminator="status"),
]

# Backward-compatible alias for clients expecting the ready shape only.
GeneratedLessonResponse = GenerateLessonReadyResponse


def resolve_intention(request: GenerateLessonRequest) -> str:
    if request.intention and request.intention.strip():
        return request.intention.strip()

    if request.primary_goal and request.primary_goal.strip():
        intention_parts = [request.primary_goal.strip()]
        if request.secondary_goals:
            intention_parts.append("; ".join(goal.strip() for goal in request.secondary_goals if goal.strip()))
        return ". ".join(intention_parts)

    return ""
