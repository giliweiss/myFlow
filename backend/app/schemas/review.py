from pydantic import BaseModel


class ReviewBase(BaseModel):
    lesson_id: str
    perceived_difficulty: int


class Review(ReviewBase):
    id: str

    class Config:
        from_attributes = True
