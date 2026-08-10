from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

from app.api.dependencies import get_exercise_repository
from app.core.auth import get_current_user
from app.repositories.exercise_repo import ExerciseRepository
from app.schemas.exercise import ExerciseListResponse, ExerciseResponse

router = APIRouter()


class FilterExercisesRequest(BaseModel):
    group_id: str
    level: str
    available_equipment: list[str] = []
    group_considerations: list[str] = []


@router.get("", response_model=ExerciseListResponse)
async def list_exercises(
    user: dict = Depends(get_current_user),
    exercise_repository: ExerciseRepository = Depends(get_exercise_repository),
):
    """List all active exercises in the catalog."""
    exercises = exercise_repository.list_active()
    return ExerciseListResponse(
        exercises=[ExerciseResponse(**exercise) for exercise in exercises],
        count=len(exercises),
    )


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: str,
    user: dict = Depends(get_current_user),
    exercise_repository: ExerciseRepository = Depends(get_exercise_repository),
):
    """Get a single exercise by ID."""
    exercise = exercise_repository.get_by_id(exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ExerciseResponse(**exercise)


@router.post("/filter")
def filter_exercises(request: FilterExercisesRequest = Body(...)):
    """Filter exercises by group context."""
    return {
        "exercises": [],
        "restrictions": {},
        "message": "filter endpoint - to be implemented in Phase 1",
    }


@router.post("/seed")
def seed_exercises():
    """Seed exercise database from import file."""
    return {"message": "seed endpoint - to be implemented in Phase 1"}
