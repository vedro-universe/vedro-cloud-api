from datetime import datetime

from ..clients.postgresql import PostgreSQL
from ..models.report import Report
from .base import BaseRepository

__all__ = ("ReportRepository",)


class ReportRepository(BaseRepository):
    def __init__(self, pgsql: PostgreSQL) -> None:
        super().__init__()
        self._pgsql = pgsql

    async def create(self, report: Report) -> None:
        query = """
            INSERT INTO reports (id, project_id, created_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
        """

        created_at = datetime.utcnow()
        async with self._pgsql.connection() as conn:
            await conn.execute(query, report.id, report.project_id, created_at)
