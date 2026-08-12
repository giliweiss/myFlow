from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_instructor_profile_repository
from app.core.auth import get_current_user
from app.repositories.instructor_profile_repo import InstructorProfileRepository
from app.schemas.instructor_profile import (
    InstructorProfileResponse,
    UpsertInstructorProfileRequest,
)

router = APIRouter()


@router.get("", response_model=InstructorProfileResponse)
async def get_instructor_profile(
    user: dict = Depends(get_current_user),
    instructor_profile_repository: InstructorProfileRepository = Depends(
        get_instructor_profile_repository
    ),
):
    """Get the authenticated instructor's profile."""
    profile = instructor_profile_repository.get_by_id(user["user_id"])
    if profile is None:
        raise HTTPException(status_code=404, detail="Instructor profile not found")
    return InstructorProfileResponse(**profile)


@router.post("", response_model=InstructorProfileResponse)
async def upsert_instructor_profile(
    request: UpsertInstructorProfileRequest,
    user: dict = Depends(get_current_user),
    instructor_profile_repository: InstructorProfileRepository = Depends(
        get_instructor_profile_repository
    ),
):
    """Create or update the authenticated instructor's profile."""
    profile = instructor_profile_repository.upsert(
        user["user_id"],
        request.display_name,
    )
    return InstructorProfileResponse(**profile)
