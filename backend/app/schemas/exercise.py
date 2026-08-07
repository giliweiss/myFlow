from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    description: str | None = None


class Exercise(ExerciseBase):
    id: str

    class Config:
        from_attributes = True
