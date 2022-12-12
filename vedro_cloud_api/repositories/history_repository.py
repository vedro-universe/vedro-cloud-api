from datetime import datetime, timedelta
from typing import Dict, List, TypedDict
from uuid import UUID

from asyncpg.exceptions import UndefinedTableError

from ..clients import PgsqlClient
from ..utils import cut_str
from .repository import Repository

__all__ = ("HistoryRepository", "HistoryEntity")


class HistoryEntity(TypedDict):
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


class HistoryRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    def _make_table_name(self, project_id: str) -> str:
        project_id = project_id.replace("-", "_")
        return f"history_{project_id}"

    async def save_history_entities(self, project_id: str,
                                    history: List[HistoryEntity]) -> None:
        table_name = self._make_table_name(project_id)
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} (LIKE history INCLUDING ALL)"

        insert_query = f"""
            INSERT INTO {table_name} (
                id,
                launch_id,
                report_id,
                report_hash,

                scenario_hash,
                scenario_path,
                scenario_subject,

                status,
                started_at,
                ended_at,
                duration
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """
        args = []
        for entity in history:
            args.append([
                entity["id"],
                entity["launch_id"],
                cut_str(entity["report_id"], 255),
                entity["report_hash"],

                entity["scenario_hash"],
                cut_str(entity["scenario_path"], 255),
                cut_str(entity["scenario_subject"], 255),

                entity["status"],
                entity["started_at"],
                entity["ended_at"],
                entity["ended_at"] - entity["started_at"]
            ])

        async with self._pgsql_client.transaction() as conn:
            await conn.execute(create_query)
            await conn.executemany(insert_query, args)

    async def get_scenarios(self, project_id: str, order_by: str) -> List[Dict[str, str | int]]:
        assert order_by in ("duration",)

        table_name = self._make_table_name(project_id)
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
