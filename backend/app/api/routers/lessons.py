"""Lesson endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user

router = APIRouter()


class UpdateLessonRequest(BaseModel):
    title: str | None = None
    status: str | None = None
    duration_minutes: int | None = None
    intensity_target: int | None = None
    notes: str | None = None


class ReplaceExerciseRequest(BaseModel):
    new_exercise_id: str


class SubmitReviewRequest(BaseModel):
    perceived_difficulty: int
    group_response: str  # too_easy, appropriate, too_hard, mixed
    goals_achieved: list[str] = []
    issues: str | None = None
    instructor_notes: str | None = None


@router.get("/{lesson_id}")
async def get_lesson(lesson_id: str, user: dict = Depends(get_current_user)):
    """Get a lesson by ID."""
    # TODO: LessonRepository.get_by_id(lesson_id)
    # TODO: verify user owns the group this lesson belongs to
    return {"lesson": {}, "message": "get lesson - Phase 1"}


@router.patch("/{lesson_id}")
async def update_lesson(
    lesson_id: str,
    request: UpdateLessonRequest,
    user: dict = Depends(get_current_user),
):
    """Update a lesson."""
    # TODO: verify user owns the group
    # TODO: LessonRepository.update(lesson_id, request.dict(exclude_unset=True))
    return {"lesson": {}, "message": "update lesson - Phase 1"}


@router.post("/{lesson_id}/exercises/{item_id}/replace")
async def replace_exercise(
    lesson_id: str,
    item_id: str,
    request: ReplaceExerciseRequest,
    user: dict = Depends(get_current_user),
):
    """Replace an exercise in a lesson."""
    # TODO: verify user owns the group
    # TODO: LessonRepository.update_exercise(item_id, request.new_exercise_id)
    return {"lesson": {}, "message": "replace exercise - Phase 1"}


@router.post("/{lesson_id}/review")
async def submit_lesson_review(
    lesson_id: str,
    request: SubmitReviewRequest,
    user: dict = Depends(get_current_user),
):
    """Submit a review for a taught lesson."""
    # TODO: verify user owns the group
    # TODO: LessonRepository.update_status(lesson_id, "taught")
    # TODO: ReviewRepository.create(lesson_id, request.dict())
    return {"review": {}, "message": "submit review - Phase 1"}
