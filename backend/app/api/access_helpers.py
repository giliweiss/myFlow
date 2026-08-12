"""Shared ownership checks for group-scoped resources."""

from fastapi import HTTPException, status

from app.core.auth import verify_instructor_ownership
from app.repositories.group_repo import GroupRepository
from app.repositories.lesson_repo import LessonRepository


def get_owned_group(
    group_id: str,
    user: dict,
    group_repository: GroupRepository,
) -> dict:
    group = group_repository.get_by_id(group_id)
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not verify_instructor_ownership(user, group["instructor_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return group


def get_owned_lesson(
    lesson_id: str,
    user: dict,
    lesson_repository: LessonRepository,
    group_repository: GroupRepository,
) -> tuple[dict, dict]:
    lesson = lesson_repository.get_by_id(lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    group = get_owned_group(lesson["group_id"], user, group_repository)
    return lesson, group
