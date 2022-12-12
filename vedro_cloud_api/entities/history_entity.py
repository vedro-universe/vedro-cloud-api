from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .entity import Entity

__all__ = ("HistoryEntity",)


@dataclass
class HistoryEntity(Entity):
    id: UUID
    launch_id: UUID
    report_id: str
    report_hash: str

    scenario_hash: str
    scenario_path: str
    scenario_subject: str

    status: str
    started_at: datetime
    ended_at: datetime
