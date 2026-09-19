from typing import Literal

from pydantic import BaseModel, Field


class InstructorExerciseResponse(BaseModel):
    id: str
    instructor_id: str
    name_he: str
    name_en: str | None = None
    description_he: str | None = None
    difficulty_level: str
    body_focus: list[str]
    possible_equipment: list[str]
    teaching_notes: str | None = None
    source: str
    based_on_catalog_exercise_id: str | None = None
    based_on_modification: str | None = None
    is_archived: bool
    created_at: str
    updated_at: str


class InstructorExerciseListResponse(BaseModel):
    exercises: list[InstructorExerciseResponse]
    count: int


class CreateInstructorExerciseRequest(BaseModel):
    name_he: str = Field(min_length=1)
    name_en: str | None = None
    description_he: str | None = None
    difficulty_level: Literal["beginner", "intermediate", "advanced"]
    body_focus: list[str] = Field(default_factory=list)
    possible_equipment: list[str] = Field(default_factory=list)
    teaching_notes: str | None = None
    source: Literal["manual", "ai_saved"] = "manual"
    based_on_catalog_exercise_id: str | None = None
    based_on_modification: str | None = None


class UpdateInstructorExerciseRequest(BaseModel):
    name_he: str | None = Field(default=None, min_length=1)
    name_en: str | None = None
    description_he: str | None = None
    difficulty_level: Literal["beginner", "intermediate", "advanced"] | None = None
    body_focus: list[str] | None = None
    possible_equipment: list[str] | None = None
    teaching_notes: str | None = None
    is_archived: bool | None = None
