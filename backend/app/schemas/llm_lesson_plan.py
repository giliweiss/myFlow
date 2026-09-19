from typing import Literal

from pydantic import BaseModel, Field


class LLMClarificationQuestion(BaseModel):
    question_id: str
    prompt: str
    why_needed: str | None = None


class LLMClarificationOutput(BaseModel):
    clarification_questions: list[LLMClarificationQuestion] = Field(min_length=1, max_length=2)


class LLMGeneratedExerciseAlternative(BaseModel):
    exercise_id: str = Field(description="UUID of an alternative exercise from the provided catalog")
    relation_type: Literal["alternative", "regression", "progression"] = "alternative"
    reason: str | None = None


class LLMGeneratedLessonExercise(BaseModel):
    exercise_id: str = Field(description="UUID of an exercise from the preparation catalog only")
    order_index: int = Field(ge=0)
    section: Literal["warmup", "main", "cooldown"]
    planned_duration_seconds: int | None = Field(default=None, gt=0)
    sets: int | None = Field(default=None, gt=0)
    reps: int | None = Field(default=None, gt=0)
    selected_modification: str | None = None
    instructor_notes: str | None = None
    alternatives: list[LLMGeneratedExerciseAlternative] = Field(default_factory=list)


class LLMExerciseGuidance(BaseModel):
    exercise_id: str
    why_chosen: str | None = None
    progression_role: str | None = None
    teaching_cues: list[str] = Field(default_factory=list)
    creative_variations: list[str] = Field(default_factory=list)


class LLMSectionNote(BaseModel):
    section: Literal["warmup", "main", "cooldown"]
    note: str = Field(min_length=1)


class LLMLessonGuidance(BaseModel):
    lesson_strategy: str | None = None
    structure_rationale: str | None = None
    progression_logic: str | None = None
    section_notes: list[LLMSectionNote] = Field(default_factory=list)
    exercise_guidance: list[LLMExerciseGuidance] = Field(default_factory=list)


class LLMReadyLessonPlan(BaseModel):
    title: str = Field(min_length=1)
    primary_goal: str = Field(min_length=1)
    secondary_goals: list[str] = Field(default_factory=list)
    lesson_exercises: list[LLMGeneratedLessonExercise] = Field(default_factory=list)
    guidance: LLMLessonGuidance


class LLMPlanningOutput(BaseModel):
    status: Literal["needs_clarification", "ready"]
    clarification_questions: list[LLMClarificationQuestion] = Field(default_factory=list, max_length=2)
    title: str | None = None
    primary_goal: str | None = None
    secondary_goals: list[str] = Field(default_factory=list)
    lesson_exercises: list[LLMGeneratedLessonExercise] = Field(default_factory=list)
    guidance: LLMLessonGuidance | None = None


# Legacy alias used by older tests and validation helpers.
LLMGeneratedLessonPlan = LLMReadyLessonPlan
