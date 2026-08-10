from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    id: str
    canonical_key: str
    name_en: str
    name_he: str
    description_en: str | None = None
    description_he: str | None = None
    difficulty_level: str
    body_focus: list[str]
    position: str | None = None
    possible_equipment: list[str]
    intensity: int | None = None
    min_duration_seconds: int | None = None
    max_duration_seconds: int | None = None
    min_reps: int | None = None
    max_reps: int | None = None
    phase_affinities: list[str]
    teaching_cues_en: list[str]
    teaching_cues_he: list[str]
    common_mistakes_en: list[str]
    common_mistakes_he: list[str]
    aliases_en: list[str]
    aliases_he: list[str]
    pilates_principles: list[str]
    is_active: bool


class ExerciseListResponse(BaseModel):
    exercises: list[ExerciseResponse]
    count: int
