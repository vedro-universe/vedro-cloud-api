from datetime import timedelta
from typing import Dict, List

from asyncpg.exceptions import UndefinedTableError

from ..clients import PgsqlClient
from ..entities import HistoryEntity
from .repository import Repository

__all__ = ("HistoryRepository",)


class HistoryRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    async def save_history_entities(self, project_id: str,
                                    history_entities: List[HistoryEntity]) -> None:
        table_name = f"history_{project_id}"
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} (LIKE history INCLUDING ALL)"

        insert_query = f"""
            INSERT INTO {table_name} (
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
        args = []
        for history_entity in history_entities:
            args.append([
                history_entity.id,
                history_entity.scenario_id,
                history_entity.scenario_hash,
                history_entity.scenario_path,
                history_entity.scenario_subject,
                history_entity.status,
                history_entity.started_at,
                history_entity.ended_at,
                history_entity.ended_at - history_entity.started_at
            ])

        async with self._pgsql_client.transaction() as conn:
            await conn.execute(create_query)
            await conn.executemany(insert_query, args)

    async def get_scenarios(self, project_id: str, order_by: str) -> List[Dict[str, str | int]]:
        assert order_by in ("duration",)

        table_name = f"history_{project_id}"
        query = f"""
            WITH stats AS (
                SELECT
                    scenario_hash,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration) AS median
                FROM {table_name}
                GROUP BY scenario_hash
            )
            SELECT
                DISTINCT(h.scenario_hash),
                median
            FROM {table_name} AS h
            JOIN stats AS s
                ON h.scenario_hash = s.scenario_hash
            ORDER BY median DESC
        """

        results: List[Dict[str, str | int]] = []
        async with self._pgsql_client.connection() as conn:
            try:
                records = await conn.fetch(query)
            except UndefinedTableError:
                return results
            for record in records:
                results.append({
                    "scenario_hash": record["scenario_hash"],
                    "median": int(record["median"] / timedelta(milliseconds=1)),
                })

        return results
