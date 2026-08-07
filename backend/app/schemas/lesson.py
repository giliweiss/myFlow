from pydantic import BaseModel


class LessonBase(BaseModel):
    title: str
    group_id: str


class Lesson(LessonBase):
    id: str
    status: str

    class Config:
        from_attributes = True
