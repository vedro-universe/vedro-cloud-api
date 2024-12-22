import json
from datetime import datetime
from uuid import UUID

from ..clients.postgresql import PostgreSQL
from ..models.scenario_result import ScenarioResult
from .base import BaseRepository

__all__ = ("ScenarioResultRepository",)


class ScenarioResultRepository(BaseRepository):
    def __init__(self, pgsql: PostgreSQL) -> None:
        super().__init__()
        self._pgsql = pgsql

    async def create(self, scenario_result: ScenarioResult, launch_id: UUID) -> None:
        query = """
            INSERT INTO scenario_results (
                id,
                launch_id,
                status,
                started_at,
                ended_at,
                scenario,
                step_results,
                created_at
            )
            VALUES (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6,
                $7,
                $8
            )
            ON CONFLICT (id) DO NOTHING
        """

        scenario_data = scenario_result.scenario.model_dump()
        step_results_data = [step_result.model_dump()
                             for step_result in scenario_result.step_results]

        created_at = datetime.utcnow()
        async with self._pgsql.connection() as conn:
            await conn.execute(
                query,
                scenario_result.id,
                launch_id,
                scenario_result.status,
                scenario_result.started_at,
                scenario_result.ended_at,
                json.dumps(scenario_data),
                json.dumps(step_results_data),
                created_at
            )
