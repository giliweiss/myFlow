from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class SubmitReviewRequest(BaseModel):
    perceived_difficulty: int = Field(ge=1, le=5)
    group_response: Literal["too_easy", "appropriate", "too_hard", "mixed"]
    goals_achieved: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    instructor_notes: str | None = None


class ReviewResponse(BaseModel):
    id: str
    lesson_id: str
    perceived_difficulty: int
    group_response: str
    goals_achieved: list[str]
    issues: list[str]
    instructor_notes: str | None = None
    created_at: datetime
    updated_at: datetime
