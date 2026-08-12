"""Group endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.access_helpers import get_owned_group
from app.api.dependencies import (
    get_attendance_service,
    get_group_member_repository,
    get_group_repository,
    get_instructor_profile_repository,
)
from app.core.auth import get_current_user
from app.repositories.group_member_repo import GroupMemberRepository
from app.repositories.group_repo import GroupRepository
from app.repositories.instructor_profile_repo import InstructorProfileRepository
from app.schemas.group import (
    CreateGroupRequest,
    GroupListResponse,
    GroupResponse,
    UpdateGroupRequest,
)
from app.schemas.group_member import (
    CreateGroupMemberRequest,
    GroupMemberListResponse,
    GroupMemberResponse,
    UpdateGroupMemberRequest,
)
from app.services.attendance_service import AttendanceService

router = APIRouter()


def require_instructor_profile(
    user_id: str,
    instructor_profile_repository: InstructorProfileRepository,
) -> dict:
    profile = instructor_profile_repository.get_by_id(user_id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Instructor profile required. "
                "Create one with POST /instructor-profile before creating groups."
            ),
        )
    return profile


@router.get("", response_model=GroupListResponse)
async def list_groups(
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
):
    """List all active groups for the authenticated instructor."""
    groups = group_repository.list_by_instructor(user["user_id"])
    return GroupListResponse(
        groups=[GroupResponse(**group) for group in groups],
        count=len(groups),
    )


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    request: CreateGroupRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    instructor_profile_repository: InstructorProfileRepository = Depends(
        get_instructor_profile_repository
    ),
):
    """Create a new group for the authenticated instructor."""
    require_instructor_profile(user["user_id"], instructor_profile_repository)

    group = group_repository.create(
        user["user_id"],
        request.model_dump(mode="json"),
    )
    return GroupResponse(**group)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: str,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
):
    """Get a group by ID."""
    group = get_owned_group(group_id, user, group_repository)
    return GroupResponse(**group)


@router.patch("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: str,
    request: UpdateGroupRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
):
    """Update a group."""
    get_owned_group(group_id, user, group_repository)

    update_data = request.model_dump(mode="json", exclude_unset=True)
    if not update_data:
        group = group_repository.get_by_id(group_id)
        return GroupResponse(**group)

    group = group_repository.update(group_id, update_data)
    return GroupResponse(**group)


@router.get("/{group_id}/members", response_model=GroupMemberListResponse)
async def list_group_members(
    group_id: str,
    include_inactive: bool = Query(default=False),
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    group_member_repository: GroupMemberRepository = Depends(get_group_member_repository),
):
    """List members for a group."""
    get_owned_group(group_id, user, group_repository)
    members = group_member_repository.list_by_group(group_id, include_inactive=include_inactive)
    return GroupMemberListResponse(
        members=[GroupMemberResponse(**member) for member in members],
        count=len(members),
    )


@router.post(
    "/{group_id}/members",
    response_model=GroupMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group_member(
    group_id: str,
    request: CreateGroupMemberRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    group_member_repository: GroupMemberRepository = Depends(get_group_member_repository),
    attendance_service: AttendanceService = Depends(get_attendance_service),
):
    """Add a member to a group roster."""
    get_owned_group(group_id, user, group_repository)
    member = group_member_repository.create(group_id, request.name)
    attendance_service.add_attendance_for_new_member(group_id, member["id"])
    return GroupMemberResponse(**member)


@router.patch("/{group_id}/members/{member_id}", response_model=GroupMemberResponse)
async def update_group_member(
    group_id: str,
    member_id: str,
    request: UpdateGroupMemberRequest,
    user: dict = Depends(get_current_user),
    group_repository: GroupRepository = Depends(get_group_repository),
    group_member_repository: GroupMemberRepository = Depends(get_group_member_repository),
):
    """Rename or deactivate a group member."""
    get_owned_group(group_id, user, group_repository)

    member = group_member_repository.get_by_id_for_group(group_id, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    update_data = request.model_dump(mode="json", exclude_unset=True)
    if not update_data:
        return GroupMemberResponse(**member)

    updated_member = group_member_repository.update(member_id, update_data)
    return GroupMemberResponse(**updated_member)


@router.get("/{group_id}/progress")
async def get_group_progress(group_id: str, user: dict = Depends(get_current_user)):
    """Get progress summary for a group."""
    return {"progress": {}, "message": "group progress - Phase 2"}
