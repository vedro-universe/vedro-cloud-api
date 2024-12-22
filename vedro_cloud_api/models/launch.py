from pydantic import BaseModel, Field

from .scenario_result import ScenarioResult

__all__ = ("Launch",)


class Launch(BaseModel):
    id: str = Field(..., max_length=64)
    report_id: str = Field(..., max_length=64)

    scenario_results: list[ScenarioResult]
