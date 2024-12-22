from pydantic import BaseModel, Field

__all__ = ("Project",)


class Project(BaseModel):
    id: str = Field(..., max_length=64)
