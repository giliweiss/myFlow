from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()


class FilterExercisesRequest(BaseModel):
    group_id: str
    level: str
    available_equipment: list[str] = []
    group_considerations: list[str] = []


@router.post("/filter")
def filter_exercises(request: FilterExercisesRequest = Body(...)):
    """Filter exercises by group context."""
    return {
        "exercises": [],
        "restrictions": {},
        "message": "filter endpoint - to be implemented in Phase 1"
    }


@router.post("/seed")
def seed_exercises():
    """Seed exercise database from import file."""
    return {"message": "seed endpoint - to be implemented in Phase 1"}
