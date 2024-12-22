from datetime import UTC, datetime

from ..clients.postgresql import PostgreSQL
from ..models.project import Project
from .base import BaseRepository

__all__ = ("ProjectRepository",)


class ProjectRepository(BaseRepository):
    def __init__(self, pgsql: PostgreSQL) -> None:
        super().__init__()
        self._pgsql = pgsql

    async def create(self, project: Project) -> None:
        query = """
            INSERT INTO projects (id, name, created_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
        """

        created_at = datetime.now(UTC)
        async with self._pgsql.connection() as conn:
            await conn.execute(query, project.id, project.id, created_at)
