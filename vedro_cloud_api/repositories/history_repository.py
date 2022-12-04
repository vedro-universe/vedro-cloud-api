from datetime import timedelta
from typing import Dict, List

from ..clients import PgsqlClient
from ..entities import HistoryEntity
from .repository import Repository

__all__ = ("HistoryRepository",)


class HistoryRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    async def save_history_entities(self, history_entities: List[HistoryEntity]) -> None:
        for history_entity in history_entities:
            await self.save_history_entity(history_entity)

    async def save_history_entity(self, history_entity: HistoryEntity) -> None:
        query = """
            INSERT INTO history (
                id,
                scenario_id,
                scenario_hash,
                scenario_path,
                scenario_subject,
                status,
                started_at,
                ended_at,
                duration
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """
        async with self._pgsql_client.acquire() as conn:
            await conn.execute(
                query,
                history_entity.id,
                history_entity.scenario_id,
                history_entity.scenario_hash,
                history_entity.scenario_path,
                history_entity.scenario_subject,
                history_entity.status,
                history_entity.started_at,
                history_entity.ended_at,
                history_entity.ended_at - history_entity.started_at,
            )

    async def get_slow_scenarios(self) -> List[Dict[str, str | int]]:
        query = """
            WITH stats AS (
                SELECT
                    scenario_hash,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration) AS median
                FROM public.history
                GROUP BY scenario_hash
            )
            SELECT
                DISTINCT(h.scenario_hash),
                median
            FROM history AS h
            JOIN stats AS s
                ON h.scenario_hash = s.scenario_hash
            ORDER BY median DESC
        """

        results = []
        async with self._pgsql_client.acquire() as conn:
            records = await conn.fetch(query)
            for record in records:
                results.append({
                    "scenario_hash": record["scenario_hash"],
                    "median": int(record["median"] / timedelta(milliseconds=1)),
                })

        return results
