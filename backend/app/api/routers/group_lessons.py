"""Group-scoped lesson endpoints (list, create, generate)."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.access_helpers import get_owned_group
from app.api.dependencies import (
    get_exercise_repository,
    get_group_repository,
    get_lesson_exercise_repository,
    get_lesson_generator_service,
    get_lesson_repository,
)
from app.core.auth import get_current_user
from app.repositories.exercise_repo import ExerciseRepository
from app.repositories.group_repo import GroupRepository
from app.repositories.lesson_exercise_repo import LessonExerciseRepository
from app.repositories.lesson_repo import LessonRepository
from app.schemas.lesson import (
    CreateLessonRequest,
    LessonListResponse,
    LessonResponse,
    LessonSummary,
)
from app.schemas.lesson_generation import (
    GenerateLessonClarificationResponse,
    GenerateLessonReadyResponse,
    GenerateLessonRequest,
    GenerateLessonResponse,
)
from app.services.lesson_generator import LessonGeneratorService
from app.services.lesson_service import (
    build_lesson_response,
    exercise_items_from_input,
    validate_exercises_for_group,
    validate_lesson_exercises,
)

router = APIRouter()


@router.get("/{group_id}/lessons", response_model=LessonListResponse)
async def list_group_lessons(
    group_id: str,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
):
    """List all lessons for a group."""
    get_owned_group(group_id, user, group_repository)
    lessons = lesson_repository.list_summaries_by_group(group_id)

    summaries = []
    for lesson in lessons:
        has_review = bool(lesson.get("lesson_reviews"))
        summaries.append(
            LessonSummary(
                id=lesson["id"],
                group_id=lesson["group_id"],
                title=lesson["title"],
                status=lesson["status"],
                scheduled_for=lesson.get("scheduled_for"),
                planned_duration_minutes=lesson.get("planned_duration_minutes"),
                created_at=lesson["created_at"],
                updated_at=lesson["updated_at"],
                has_review=has_review,
            )
        )

    return LessonListResponse(lessons=summaries, count=len(summaries))


@router.post(
    "/{group_id}/lessons",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group_lesson(
    group_id: str,
    request: CreateLessonRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    lesson_exercise_repository: LessonExerciseRepository = Depends(get_lesson_exercise_repository),
    exercise_repository: ExerciseRepository = Depends(get_exercise_repository),
):
    """Create an upcoming lesson with structured exercises."""
    group = get_owned_group(group_id, user, group_repository)

    exercise_items = exercise_items_from_input(request.lesson_exercises)
    lesson_data = request.model_dump(mode="json", exclude={"lesson_exercises"})
    lesson_data["level"] = request.level or group["level"]

    if lesson_data.get("planned_duration_minutes") is None:
        lesson_data["planned_duration_minutes"] = group["typical_duration_minutes"]

    validate_exercises_for_group(exercise_items, group, exercise_repository)
    validate_lesson_exercises(lesson_data, exercise_items, exercise_repository, for_plan=False)

    lesson = lesson_repository.create(group_id, lesson_data)
    exercises = lesson_exercise_repository.replace_for_lesson(lesson["id"], exercise_items)
    return build_lesson_response(lesson, exercises)


@router.post(
    "/{group_id}/lessons/generate",
    response_model=GenerateLessonClarificationResponse | GenerateLessonReadyResponse,
)
async def generate_lesson(
    group_id: str,
    request: GenerateLessonRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_generator_service: LessonGeneratorService = Depends(get_lesson_generator_service),
) -> GenerateLessonResponse:
    """Generate a lesson plan for a group without persisting it."""
    group = get_owned_group(group_id, user, group_repository)
    return lesson_generator_service.generate(group_id, group, request)
