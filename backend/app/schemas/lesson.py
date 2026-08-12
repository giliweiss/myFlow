from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.review import ReviewResponse


class LessonExerciseInput(BaseModel):
    exercise_id: str
    order_index: int = Field(ge=0)
    section: Literal["warmup", "main", "cooldown"]
    planned_duration_seconds: int | None = Field(default=None, gt=0)
    sets: int | None = Field(default=None, gt=0)
    reps: int | None = Field(default=None, gt=0)
    selected_modification: str | None = None
    instructor_notes: str | None = None


class LessonExerciseCompletionInput(BaseModel):
    id: str
    completion_status: Literal["completed", "shortened", "skipped"]
    actual_duration_seconds: int | None = Field(default=None, gt=0)


class LessonExerciseResponse(BaseModel):
    id: str
    lesson_id: str
    exercise_id: str
    order_index: int
    section: str
    planned_duration_seconds: int | None = None
    actual_duration_seconds: int | None = None
    sets: int | None = None
    reps: int | None = None
    selected_modification: str | None = None
    instructor_notes: str | None = None
    completion_status: str | None = None


class AttendanceMemberSummary(BaseModel):
    id: str
    name: str
    is_active: bool


class AttendanceResponse(BaseModel):
    id: str
    lesson_id: str
    group_member_id: str
    registered: bool
    attended: bool
    member: AttendanceMemberSummary | None = None


class CreateLessonRequest(BaseModel):
    title: str = Field(min_length=1)
    primary_goal: str | None = None
    secondary_goals: list[str] = Field(default_factory=list)
    level: Literal["beginner", "intermediate", "advanced"] | None = None
    planned_duration_minutes: int | None = Field(default=None, gt=0)
    instructor_notes: str | None = None
    lesson_exercises: list[LessonExerciseInput] = Field(default_factory=list)


class UpdateLessonRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    status: Literal["draft", "planned", "taught", "cancelled"] | None = None
    scheduled_for: datetime | None = None
    primary_goal: str | None = None
    secondary_goals: list[str] | None = None
    level: Literal["beginner", "intermediate", "advanced"] | None = None
    planned_duration_minutes: int | None = Field(default=None, gt=0)
    actual_duration_minutes: int | None = Field(default=None, gt=0)
    instructor_notes: str | None = None
    lesson_exercises: list[LessonExerciseInput] | None = None
    exercise_completions: list[LessonExerciseCompletionInput] | None = None


class LessonSummary(BaseModel):
    id: str
    group_id: str
    title: str
    status: str
    scheduled_for: datetime | None = None
    created_at: datetime
    updated_at: datetime
    has_review: bool


class LessonListResponse(BaseModel):
    lessons: list[LessonSummary]
    count: int


class LessonResponse(BaseModel):
    id: str
    group_id: str
    title: str
    status: str
    scheduled_for: datetime | None = None
    primary_goal: str | None = None
    secondary_goals: list[str]
    level: str
    planned_duration_minutes: int | None = None
    actual_duration_minutes: int | None = None
    instructor_notes: str | None = None
    created_at: datetime
    updated_at: datetime
    lesson_exercises: list[LessonExerciseResponse]
    attendance: list[AttendanceResponse] = Field(default_factory=list)
    review: "ReviewResponse | None" = None


class AttendanceUpdateItem(BaseModel):
    member_id: str
    registered: bool | None = None
    attended: bool | None = None


class AttendanceUpdateRequest(BaseModel):
    attendance: list[AttendanceUpdateItem]


class AttendanceListResponse(BaseModel):
    attendance: list[AttendanceResponse]
    count: int


class ReplaceExerciseRequest(BaseModel):
    new_exercise_id: str


from app.schemas.review import ReviewResponse

LessonResponse.model_rebuild()
