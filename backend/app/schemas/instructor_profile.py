from datetime import datetime, time

from pydantic import BaseModel, Field


class InstructorProfileResponse(BaseModel):
    id: str
    display_name: str
    created_at: datetime
    updated_at: datetime


class UpsertInstructorProfileRequest(BaseModel):
    display_name: str = Field(min_length=1)
