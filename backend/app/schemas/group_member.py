from datetime import datetime

from pydantic import BaseModel, Field


class GroupMemberResponse(BaseModel):
    id: str
    group_id: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class GroupMemberListResponse(BaseModel):
    members: list[GroupMemberResponse]
    count: int


class CreateGroupMemberRequest(BaseModel):
    name: str = Field(min_length=1)


class UpdateGroupMemberRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    is_active: bool | None = None
