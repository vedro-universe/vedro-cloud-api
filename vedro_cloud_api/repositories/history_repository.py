from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, TypedDict
from uuid import UUID, uuid4

from asyncpg.exceptions import UndefinedTableError

from ..clients import PgsqlClient
from ..utils import cut_str
from .repository import Repository

__all__ = ("HistoryRepository", "HistoryEntity")


class HistoryEntity(TypedDict):
    id: UUID
    launch_id: UUID
    report_id: str
    project_id: str

    scenario_hash: str
    scenario_rel_path: str
    scenario_subject: str
    scenario_namespace: str

    status: str
    started_at: datetime
    ended_at: datetime


class HistoryRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    def _make_table_name(self, project_id: str) -> str:
        project_id = project_id.replace("-", "_")
        return f"history_{project_id}"

    def _gen_unique_id(self) -> str:
        return str(uuid4())

    def _make_create_project_query(self, project_id: str) -> Tuple[str, List[str]]:
        query = """
            INSERT INTO projects (id, created_at) VALUES ($1, NOW())
            ON CONFLICT (id) DO NOTHING
        """
        return query, [project_id]

    def _make_create_report_query(self, project_id: str, report_id: str) -> Tuple[str, List[str]]:
        query = """
            INSERT INTO reports (id, report_id, project_id, snapshot, created_at, updated_at)
            (
                SELECT
                    gen_random_uuid() as id,
                    $1 as report_id,
                    $2 as project_id,
                    (case when max(serial) is null then 0 else max(serial) END) as snapshot,
                    NOW() as created_at,
                    NOW() as updated_at
                FROM runs
            )
            ON CONFLICT (report_id, project_id) DO UPDATE SET updated_at = EXCLUDED.updated_at
            RETURNING id
        """
        return query, [report_id, project_id]

    def _make_create_scenarios_query(self, project_id: str,
                                     history: List[HistoryEntity]) -> Tuple[str, List[List[Any]]]:
        # workaround for 'invalid array element: object of type 'UUID' has no len()'
        # with unnest($1::scenarios[])
        query = """
            INSERT INTO scenarios (
                id,
                scenario_id,
                project_id,
                subject,
                namespace,
                rel_path,
                created_at,
                updated_at
            )
            (
                SELECT
                    gen_random_uuid(),
                    t.scenario_id,
                    t.project_id,
                    t.subject,
                    t.namespace,
                    t.rel_path,
                    NOW(),
                    NOW()
                FROM unnest($1::text[], $2::text[], $3::text[], $4::text[], $5::text[])
                AS t (scenario_id, project_id, subject, namespace, rel_path)
            )
            ON CONFLICT (scenario_id, project_id) DO UPDATE SET updated_at = EXCLUDED.updated_at
            RETURNING id, scenario_id
        """

        args: List[List[Any]] = [[] for _ in range(5)]
        for entity in history:
            args[0].append(entity["scenario_hash"])
            args[1].append(project_id)
            args[2].append(cut_str(entity["scenario_subject"], 255))
            args[3].append(cut_str(entity["scenario_namespace"], 255))
            args[4].append(cut_str(entity["scenario_rel_path"], 255))

        return query, args

    def _make_create_runs_query(self, project_id: str,
                                report_id: str,
                                history: List[HistoryEntity],
                                scenarios: Dict[str, str]) -> Tuple[str, List[List[Any]]]:
        query = """
            INSERT INTO runs (
                id,
                launch_id,
                report_id,
                project_id,
                scenario_id,
                status,
                started_at,
                ended_at,
                duration,
                created_at,
                updated_at
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET updated_at = EXCLUDED.updated_at
        """
        args = []
        for entity in history:
            args.append([
                entity["id"],
                entity["launch_id"],
                report_id,
                project_id,
                scenarios[entity["scenario_hash"]],
                entity["status"],
                entity["started_at"],
                entity["ended_at"],
                entity["ended_at"] - entity["started_at"],
            ])
        return query, args

    async def save_history_entities(self, project_id: str, report_id: str,
                                    history: List[HistoryEntity]) -> None:
        async with self._pgsql_client.transaction() as conn:
            project_query, project_args = self._make_create_project_query(project_id)
            await conn.execute(project_query, *project_args)

            report_query, report_args = self._make_create_report_query(project_id, report_id)
            row = await conn.fetchrow(report_query, *report_args)
            report_id = row["id"]

            scn_query, scn_args = self._make_create_scenarios_query(project_id, history)
            records = await conn.fetch(scn_query, *scn_args)
            scenarios = {record["scenario_id"]: record["id"] for record in records}

            runs_query, runs_args = self._make_create_runs_query(project_id, report_id,
                                                                 history, scenarios)
            await conn.executemany(runs_query, runs_args)

    async def get_scenarios(self, project_id: str,
                            order_by: str, report_id: str) -> List[Dict[str, str | int]]:
        assert order_by in ("duration",)

        async with self._pgsql_client.transaction() as conn:
            project_query, project_args = self._make_create_project_query(project_id)
            await conn.execute(project_query, *project_args)

            report_query, report_args = self._make_create_report_query(project_id, report_id)
            row = await conn.fetchrow(report_query, *report_args)
            report_id = row["id"]

            query = """
                WITH stats AS (
                    SELECT
                        scenario_id,
                        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration) AS median,
                        AVG(duration) as average
                    FROM runs
                    WHERE project_id = $1
                        AND status IN ('PASSED', 'FAILED')
                        AND serial <= (SELECT snapshot FROM reports WHERE id = $2)
                    GROUP BY scenario_id
                )
                SELECT
                    DISTINCT(scenarios.id),
                    scenarios.scenario_id,
                    median,average
                FROM scenarios
                JOIN stats as s
                    ON scenarios.id = s.scenario_id
                ORDER BY median DESC, average DESC
            """
            results: List[Dict[str, str | int]] = []
            try:
                records = await conn.fetch(query, project_id, report_id)
            except UndefinedTableError:
                return results
            for record in records:
                results.append({
                    "id": str(record["id"]),
                    "hash": record["scenario_id"],
                    "median": int(record["median"] / timedelta(milliseconds=1)),
                    "average": int(record["average"] / timedelta(milliseconds=1)),
                })

        return results
