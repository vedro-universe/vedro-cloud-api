from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

__all__ = ("ScenarioResult",)


class ScenarioStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class StepStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"


class Scenario(BaseModel):
    id: str
    subject: str
    rel_path: str


class StepResult(BaseModel):
    id: UUID
    status: StepStatus
    started_at: datetime
    ended_at: datetime


class ScenarioResult(BaseModel):
    id: UUID
    status: ScenarioStatus
    started_at: datetime
    ended_at: datetime

    scenario: Scenario
    step_results: list[StepResult]
