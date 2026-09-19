"""Lesson endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.access_helpers import get_owned_lesson
from app.api.dependencies import (
    get_attendance_service,
    get_exercise_repository,
    get_group_member_repository,
    get_group_repository,
    get_lesson_attendance_repository,
    get_lesson_exercise_repository,
    get_lesson_repository,
    get_review_repository,
)
from app.core.auth import get_current_user
from app.repositories.exercise_repo import ExerciseRepository
from app.repositories.group_member_repo import GroupMemberRepository
from app.repositories.group_repo import GroupRepository
from app.repositories.lesson_attendance_repo import LessonAttendanceRepository
from app.repositories.lesson_exercise_repo import LessonExerciseRepository
from app.repositories.lesson_repo import LessonRepository
from app.repositories.review_repo import ReviewRepository
from app.schemas.lesson import (
    AttendanceListResponse,
    AttendanceMemberSummary,
    AttendanceResponse,
    AttendanceUpdateRequest,
    LessonResponse,
    ReplaceExerciseRequest,
    UpdateLessonRequest,
)
from app.schemas.review import ReviewResponse, SubmitReviewRequest
from app.services.attendance_service import AttendanceService
from app.services.lesson_validator import normalize_lesson_status
from app.services.lesson_service import (
    apply_status_transition,
    exercise_items_from_input,
    load_full_lesson,
    validate_exercises_for_group,
    validate_lesson_exercises,
)

router = APIRouter()


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: str,
    user: dict = Depends(get_current_user),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_exercise_repository: LessonExerciseRepository = Depends(get_lesson_exercise_repository),
    lesson_attendance_repository: LessonAttendanceRepository = Depends(
        get_lesson_attendance_repository
    ),
    review_repository: ReviewRepository = Depends(get_review_repository),
):
    """Get a lesson by ID."""
    get_owned_lesson(lesson_id, user, lesson_repository, group_repository)
    return load_full_lesson(
        lesson_id,
        lesson_repository,
        lesson_exercise_repository,
        lesson_attendance_repository,
        review_repository,
    )


@router.patch("/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: str,
    request: UpdateLessonRequest,
    user: dict = Depends(get_current_user),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_exercise_repository: LessonExerciseRepository = Depends(get_lesson_exercise_repository),
    lesson_attendance_repository: LessonAttendanceRepository = Depends(
        get_lesson_attendance_repository
    ),
    review_repository: ReviewRepository = Depends(get_review_repository),
    exercise_repository: ExerciseRepository = Depends(get_exercise_repository),
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    """Update a lesson."""
    lesson, group = get_owned_lesson(lesson_id, user, lesson_repository, group_repository)

    if normalize_lesson_status(lesson["status"]) in {"completed", "cancelled"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update a {lesson['status']} lesson",
        )

    update_data = request.model_dump(mode="json", exclude_unset=True)
    exercise_items = None
    if request.lesson_exercises is not None:
        exercise_items = exercise_items_from_input(request.lesson_exercises)
        update_data.pop("lesson_exercises", None)

    exercise_completions = request.exercise_completions
    update_data.pop("exercise_completions", None)
    new_status = update_data.pop("status", None)

    if exercise_items is not None:
        validate_exercises_for_group(exercise_items, group, exercise_repository)
        merged_lesson = {**lesson, **update_data}
        validate_lesson_exercises(
            merged_lesson,
            exercise_items,
            exercise_repository,
            for_plan=False,
        )
        lesson_exercise_repository.replace_for_lesson(lesson_id, exercise_items)

    if exercise_completions:
        normalized_status = normalize_lesson_status(lesson["status"])
        if normalized_status != "upcoming" and new_status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exercise completions can only be set when marking a lesson as completed",
            )
        for completion in exercise_completions:
            lesson_exercise_repository.update_completion_status(
                lesson_id,
                completion.id,
                completion.completion_status,
                completion.actual_duration_seconds,
            )

    if update_data:
        lesson = lesson_repository.update(lesson_id, update_data)

    if new_status:
        lesson = apply_status_transition(
            lesson,
            group,
            new_status,
            lesson_repository,
            lesson_exercise_repository,
            exercise_repository,
            attendance_service,
        )

    return load_full_lesson(
        lesson_id,
        lesson_repository,
        lesson_exercise_repository,
        lesson_attendance_repository,
        review_repository,
    )


@router.patch("/{lesson_id}/attendance", response_model=AttendanceListResponse)
async def update_lesson_attendance(
    lesson_id: str,
    request: AttendanceUpdateRequest,
    user: dict = Depends(get_current_user),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    group_member_repository: GroupMemberRepository = Depends(get_group_member_repository),
    lesson_attendance_repository: LessonAttendanceRepository = Depends(
        get_lesson_attendance_repository
    ),
):
    """Batch update attendance for a lesson."""
    lesson, _group = get_owned_lesson(lesson_id, user, lesson_repository, group_repository)

    if normalize_lesson_status(lesson["status"]) not in {"upcoming", "completed"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance can only be updated for upcoming or completed lessons",
        )

    existing_rows = {
        row["group_member_id"]: row
        for row in lesson_attendance_repository.list_by_lesson(lesson_id)
    }

    updates = []
    for item in request.attendance:
        member = group_member_repository.get_by_id_for_group(lesson["group_id"], item.member_id)
        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Member not found: {item.member_id}",
            )

        existing_row = existing_rows.get(item.member_id)
        updates.append(
            {
                "group_member_id": item.member_id,
                "registered": item.registered
                if item.registered is not None
                else (existing_row["registered"] if existing_row else False),
                "attended": item.attended
                if item.attended is not None
                else (existing_row["attended"] if existing_row else False),
            }
        )

    lesson_attendance_repository.upsert_attendance_updates(lesson_id, updates)
    attendance_rows = lesson_attendance_repository.list_by_lesson(lesson_id)

    attendance = []
    for row in attendance_rows:
        member_data = row.get("group_members")
        attendance.append(
            AttendanceResponse(
                id=row["id"],
                lesson_id=row["lesson_id"],
                group_member_id=row["group_member_id"],
                registered=row["registered"],
                attended=row["attended"],
                member=AttendanceMemberSummary(
                    id=member_data["id"],
                    name=member_data["name"],
                    is_active=member_data["is_active"],
                )
                if member_data
                else None,
            )
        )

    return AttendanceListResponse(attendance=attendance, count=len(attendance))


@router.post("/{lesson_id}/exercises/{item_id}/replace", response_model=LessonResponse)
async def replace_exercise(
    lesson_id: str,
    item_id: str,
    request: ReplaceExerciseRequest,
    user: dict = Depends(get_current_user),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    lesson_exercise_repository: LessonExerciseRepository = Depends(get_lesson_exercise_repository),
    lesson_attendance_repository: LessonAttendanceRepository = Depends(
        get_lesson_attendance_repository
    ),
    review_repository: ReviewRepository = Depends(get_review_repository),
    exercise_repository: ExerciseRepository = Depends(get_exercise_repository),
):
    """Replace an exercise in a lesson."""
    lesson, group = get_owned_lesson(lesson_id, user, lesson_repository, group_repository)

    if normalize_lesson_status(lesson["status"]) != "upcoming":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exercises can only be replaced on upcoming lessons",
        )

    item = lesson_exercise_repository.get_by_id_for_lesson(lesson_id, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise item not found")

    new_exercise = exercise_repository.get_by_id(request.new_exercise_id)
    if new_exercise is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown exercise id")

    validate_exercises_for_group(
        [{"exercise_id": request.new_exercise_id, "order_index": 0, "section": "main"}],
        group,
        exercise_repository,
    )

    lesson_exercise_repository.update_exercise_id(item_id, request.new_exercise_id)
    return load_full_lesson(
        lesson_id,
        lesson_repository,
        lesson_exercise_repository,
        lesson_attendance_repository,
        review_repository,
    )


@router.post("/{lesson_id}/review", response_model=ReviewResponse)
async def submit_lesson_review(
    lesson_id: str,
    request: SubmitReviewRequest,
    user: dict = Depends(get_current_user),
    lesson_repository: LessonRepository = Depends(get_lesson_repository),
    group_repository: GroupRepository = Depends(get_group_repository),
    review_repository: ReviewRepository = Depends(get_review_repository),
):
    """Create or update a review for a lesson."""
    lesson, _group = get_owned_lesson(lesson_id, user, lesson_repository, group_repository)

    if normalize_lesson_status(lesson["status"]) != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reviews can only be submitted for completed lessons",
        )

    review = review_repository.upsert_for_lesson(
        lesson_id,
        request.model_dump(mode="json"),
    )
    return ReviewResponse(**review)
