from datetime import datetime

from ..clients.postgresql import PostgreSQL
from ..models.launch import Launch
from .base import BaseRepository

__all__ = ("LaunchRepository",)


class LaunchRepository(BaseRepository):
    def __init__(self, pgsql: PostgreSQL) -> None:
        super().__init__()
        self._pgsql = pgsql

    async def create(self, launch: Launch) -> None:
        query = """
            INSERT INTO launches (id, report_id, created_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
        """

        created_at = datetime.utcnow()
        async with self._pgsql.connection() as conn:
            await conn.execute(query, launch.id, launch.report_id, created_at)
