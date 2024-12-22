from pydantic import BaseModel, Field

__all__ = ("Report",)


class Report(BaseModel):
    id: str = Field(..., max_length=64)
    project_id: str = Field(..., max_length=64)
