from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    level: str


class Group(GroupBase):
    id: str
    instructor_id: str

    class Config:
        from_attributes = True
