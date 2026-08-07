"""Group endpoints."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user

router = APIRouter()


class CreateGroupRequest(BaseModel):
    name: str
    level: str
    studio_name: str | None = None
    weekday: str | None = None
    start_time: str | None = None
    typical_duration_minutes: int = 60
    goals: list[str] = []
    available_equipment: list[str] = []
    group_considerations: list[str] = []


class UpdateGroupRequest(BaseModel):
    name: str | None = None
    level: str | None = None
    studio_name: str | None = None
    weekday: str | None = None
    start_time: str | None = None
    typical_duration_minutes: int | None = None
    goals: list[str] | None = None
    available_equipment: list[str] | None = None
    group_considerations: list[str] | None = None


@router.get("")
async def list_groups(user: dict = Depends(get_current_user)):
    """List all groups for the authenticated instructor."""
    # TODO: get_current_user should return instructor_id
    # GroupRepository.list_by_instructor(instructor_id)
    return {"groups": [], "message": "list groups - Phase 1"}


@router.post("")
async def create_group(
    request: CreateGroupRequest, user: dict = Depends(get_current_user)
):
    """Create a new group."""
    # TODO: GroupRepository.create(instructor_id, request.dict())
    return {"group": {}, "message": "create group - Phase 1"}


@router.get("/{group_id}")
async def get_group(group_id: str, user: dict = Depends(get_current_user)):
    """Get a group by ID."""
    # TODO: GroupRepository.get_by_id(group_id)
    # TODO: verify user owns this group
    return {"group": {}, "message": "get group - Phase 1"}


@router.patch("/{group_id}")
async def update_group(
    group_id: str,
    request: UpdateGroupRequest,
    user: dict = Depends(get_current_user),
):
    """Update a group."""
    # TODO: verify user owns this group
    # TODO: GroupRepository.update(group_id, request.dict(exclude_unset=True))
    return {"group": {}, "message": "update group - Phase 1"}


@router.get("/{group_id}/lessons")
async def list_group_lessons(group_id: str, user: dict = Depends(get_current_user)):
    """List all lessons for a group."""
    # TODO: verify user owns this group
    # TODO: LessonRepository.list_by_group(group_id)
    return {"lessons": [], "message": "list group lessons - Phase 1"}


@router.post("/{group_id}/lessons/generate")
async def generate_lesson(
    group_id: str, user: dict = Depends(get_current_user), duration_minutes: int = 60
):
    """Generate a lesson for a group.

    Orchestrates:
    1. Load group context
    2. Load recent lesson history
    3. Load recent reviews
    4. Retrieve all exercises
    5. Filter by constraints + recency
    6. Call LLM
    7. Validate
    8. Save as draft
    9. Return result
    """
    # TODO: verify user owns this group
    # TODO: LessonGeneratorService.generate(group_id, params)
    return {"lesson": {}, "message": "generate lesson - Phase 1"}


@router.get("/{group_id}/progress")
async def get_group_progress(group_id: str, user: dict = Depends(get_current_user)):
    """Get progress summary for a group."""
    # TODO: verify user owns this group
    # TODO: ProgressService.calculate(group_id)
    return {"progress": {}, "message": "group progress - Phase 1"}
