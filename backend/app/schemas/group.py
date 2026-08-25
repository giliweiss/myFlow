from datetime import datetime, time
from typing import Literal

from pydantic import BaseModel, Field


class GroupResponse(BaseModel):
    id: str
    instructor_id: str
    name: str
    level: str
    studio_name: str | None = None
    location_notes: str | None = None
    weekday: int | None = None
    start_time: time | None = None
    typical_duration_minutes: int
    available_equipment: list[str]
    group_considerations: list[str]
    notes: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class GroupListResponse(BaseModel):
    groups: list[GroupResponse]
    count: int


class CreateGroupRequest(BaseModel):
    name: str = Field(min_length=1)
    level: Literal["beginner", "intermediate", "advanced"]
    studio_name: str | None = None
    location_notes: str | None = None
    weekday: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    typical_duration_minutes: int = Field(default=60, gt=0)
    available_equipment: list[str] = Field(default_factory=list)
    group_considerations: list[str] = Field(default_factory=list)
    notes: str | None = None


class UpdateGroupRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    level: Literal["beginner", "intermediate", "advanced"] | None = None
    studio_name: str | None = None
    location_notes: str | None = None
    weekday: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    typical_duration_minutes: int | None = Field(default=None, gt=0)
    available_equipment: list[str] | None = None
    group_considerations: list[str] | None = None
    notes: str | None = None
    is_active: bool | None = None
