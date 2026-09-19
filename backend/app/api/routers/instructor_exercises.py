"""Instructor-owned custom exercise endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_instructor_exercise_repository,
    get_instructor_profile_repository,
)
from app.api.routers.groups import require_instructor_profile
from app.core.auth import get_current_user
from app.repositories.instructor_exercise_repo import InstructorExerciseRepository
from app.repositories.instructor_profile_repo import InstructorProfileRepository
from app.schemas.instructor_exercise import (
    CreateInstructorExerciseRequest,
    InstructorExerciseListResponse,
    InstructorExerciseResponse,
    UpdateInstructorExerciseRequest,
)

router = APIRouter()


def get_owned_instructor_exercise(
    exercise_id: str,
    instructor_id: str,
    instructor_exercise_repository: InstructorExerciseRepository,
) -> dict:
    exercise = instructor_exercise_repository.get_by_id_for_instructor(
        exercise_id,
        instructor_id,
    )
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instructor exercise not found",
        )
    return exercise


@router.get("", response_model=InstructorExerciseListResponse)
async def list_instructor_exercises(
    user: dict = Depends(get_current_user),
    instructor_exercise_repository: InstructorExerciseRepository = Depends(
        get_instructor_exercise_repository
    ),
):
    """List active custom exercises for the authenticated instructor."""
    exercises = instructor_exercise_repository.list_active_by_instructor(user["user_id"])
    return InstructorExerciseListResponse(
        exercises=[InstructorExerciseResponse(**exercise) for exercise in exercises],
        count=len(exercises),
    )


@router.post(
    "",
    response_model=InstructorExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_instructor_exercise(
    request: CreateInstructorExerciseRequest,
    user: dict = Depends(get_current_user),
    instructor_exercise_repository: InstructorExerciseRepository = Depends(
        get_instructor_exercise_repository
    ),
    instructor_profile_repository: InstructorProfileRepository = Depends(
        get_instructor_profile_repository
    ),
):
    """Create a custom instructor exercise."""
    require_instructor_profile(user["user_id"], instructor_profile_repository)

    exercise = instructor_exercise_repository.create(
        user["user_id"],
        request.model_dump(mode="json"),
    )
    return InstructorExerciseResponse(**exercise)


@router.get("/{exercise_id}", response_model=InstructorExerciseResponse)
async def get_instructor_exercise(
    exercise_id: str,
    user: dict = Depends(get_current_user),
    instructor_exercise_repository: InstructorExerciseRepository = Depends(
        get_instructor_exercise_repository
    ),
):
    """Get a custom instructor exercise by ID."""
    exercise = get_owned_instructor_exercise(
        exercise_id,
        user["user_id"],
        instructor_exercise_repository,
    )
    return InstructorExerciseResponse(**exercise)


@router.patch("/{exercise_id}", response_model=InstructorExerciseResponse)
async def update_instructor_exercise(
    exercise_id: str,
    request: UpdateInstructorExerciseRequest,
    user: dict = Depends(get_current_user),
    instructor_exercise_repository: InstructorExerciseRepository = Depends(
        get_instructor_exercise_repository
    ),
):
    """Update a custom instructor exercise."""
    get_owned_instructor_exercise(
        exercise_id,
        user["user_id"],
        instructor_exercise_repository,
    )

    update_data = request.model_dump(mode="json", exclude_unset=True)
    if not update_data:
        exercise = instructor_exercise_repository.get_by_id_for_instructor(
            exercise_id,
            user["user_id"],
        )
        return InstructorExerciseResponse(**exercise)

    exercise = instructor_exercise_repository.update(
        exercise_id,
        user["user_id"],
        update_data,
    )
    return InstructorExerciseResponse(**exercise)


@router.delete("/{exercise_id}", response_model=InstructorExerciseResponse)
async def archive_instructor_exercise(
    exercise_id: str,
    user: dict = Depends(get_current_user),
    instructor_exercise_repository: InstructorExerciseRepository = Depends(
        get_instructor_exercise_repository
    ),
):
    """Archive a custom instructor exercise."""
    get_owned_instructor_exercise(
        exercise_id,
        user["user_id"],
        instructor_exercise_repository,
    )

    exercise = instructor_exercise_repository.archive(exercise_id, user["user_id"])
    return InstructorExerciseResponse(**exercise)
