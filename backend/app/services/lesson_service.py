from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.exercise_repo import ExerciseRepository
from app.repositories.group_member_repo import GroupMemberRepository
from app.repositories.lesson_attendance_repo import LessonAttendanceRepository
from app.repositories.lesson_exercise_repo import LessonExerciseRepository
from app.repositories.lesson_repo import LessonRepository
from app.repositories.review_repo import ReviewRepository
from app.schemas.lesson import (
    AttendanceMemberSummary,
    AttendanceResponse,
    LessonExerciseResponse,
    LessonResponse,
)
from app.schemas.review import ReviewResponse
from app.services.attendance_service import AttendanceService
from app.services.exercise_filter import find_unsuitable_exercise_ids
from app.services.lesson_validator import (
    validate_lesson_for_plan,
    validate_lesson_for_save,
    validate_status_transition,
)


def build_lesson_response(
    lesson: dict,
    exercises: list[dict],
    attendance_rows: list[dict] | None = None,
    review: dict | None = None,
) -> LessonResponse:
    attendance = []
    for row in attendance_rows or []:
        member_data = row.get("group_members")
        member = None
        if member_data:
            member = AttendanceMemberSummary(
                id=member_data["id"],
                name=member_data["name"],
                is_active=member_data["is_active"],
            )
        attendance.append(
            AttendanceResponse(
                id=row["id"],
                lesson_id=row["lesson_id"],
                group_member_id=row["group_member_id"],
                registered=row["registered"],
                attended=row["attended"],
                member=member,
            )
        )

    review_response = ReviewResponse(**review) if review else None

    return LessonResponse(
        **lesson,
        lesson_exercises=[LessonExerciseResponse(**exercise) for exercise in exercises],
        attendance=attendance,
        review=review_response,
    )


def exercise_items_from_input(exercise_inputs: list) -> list[dict]:
    return [item.model_dump(mode="json") for item in exercise_inputs]


def validate_exercises_for_group(
    exercise_items: list[dict],
    group: dict,
    exercise_repository: ExerciseRepository,
) -> None:
    if not exercise_items:
        return

    exercise_ids = [item["exercise_id"] for item in exercise_items]
    exercises = exercise_repository.get_by_ids(exercise_ids)
    found_ids = {exercise["id"] for exercise in exercises}

    missing_ids = [exercise_id for exercise_id in exercise_ids if exercise_id not in found_ids]
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown exercise ids: {missing_ids}",
        )

    restrictions = exercise_repository.get_restrictions_by_exercise_ids(exercise_ids)
    unsuitable_ids = find_unsuitable_exercise_ids(
        exercises,
        group,
        restrictions,
        check_level=False,
    )
    if unsuitable_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exercises not suitable for this group: {unsuitable_ids}",
        )


def validate_lesson_exercises(
    lesson_data: dict,
    exercise_items: list[dict],
    exercise_repository: ExerciseRepository,
    for_plan: bool = False,
) -> None:
    exercise_ids = [item["exercise_id"] for item in exercise_items]
    exercises = exercise_repository.get_by_ids(exercise_ids)
    existing_exercise_ids = {exercise["id"] for exercise in exercises}

    if for_plan:
        validation = validate_lesson_for_plan(lesson_data, exercise_items, existing_exercise_ids)
    else:
        validation = validate_lesson_for_save(lesson_data, exercise_items, existing_exercise_ids)

    if not validation["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Lesson validation failed", "issues": validation["issues"]},
        )


def apply_status_transition(
    lesson: dict,
    group: dict,
    new_status: str,
    lesson_repository: LessonRepository,
    lesson_exercise_repository: LessonExerciseRepository,
    exercise_repository: ExerciseRepository,
    attendance_service: AttendanceService,
) -> dict:
    current_status = lesson["status"]
    transition = validate_status_transition(current_status, new_status)
    if not transition["valid"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid status transition", "issues": transition["issues"]},
        )

    if new_status == "planned" and current_status == "draft":
        exercises = lesson_exercise_repository.list_by_lesson(lesson["id"])
        exercise_items = [
            {
                "exercise_id": exercise["exercise_id"],
                "order_index": exercise["order_index"],
                "section": exercise["section"],
            }
            for exercise in exercises
        ]
        validate_lesson_exercises(lesson, exercise_items, exercise_repository, for_plan=True)

        update_data: dict = {"status": "planned"}
        if lesson.get("scheduled_for") is None:
            update_data["scheduled_for"] = datetime.now(timezone.utc).isoformat()

        updated_lesson = lesson_repository.update(lesson["id"], update_data)
        attendance_service.seed_attendance_for_planned_lesson(lesson["id"], group["id"])
        return updated_lesson

    return lesson_repository.update(lesson["id"], {"status": new_status})


def load_full_lesson(
    lesson_id: str,
    lesson_repository: LessonRepository,
    lesson_exercise_repository: LessonExerciseRepository,
    lesson_attendance_repository: LessonAttendanceRepository,
    review_repository: ReviewRepository,
) -> LessonResponse:
    lesson = lesson_repository.get_by_id(lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    exercises = lesson_exercise_repository.list_by_lesson(lesson_id)
    attendance = lesson_attendance_repository.list_by_lesson(lesson_id)
    review = review_repository.get_by_lesson_id(lesson_id)
    return build_lesson_response(lesson, exercises, attendance, review)
