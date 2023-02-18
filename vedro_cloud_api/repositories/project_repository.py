from datetime import datetime
from typing import List, TypedDict
from uuid import UUID

from ..clients import PgsqlClient
from .repository import Repository

__all__ = ("ProjectRepository", "ProjectEntity",)


class ProjectEntity(TypedDict):
    id: UUID
    name: str
    created_at: datetime


class ProjectRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    async def get_projects(self) -> List[ProjectEntity]:
        query = """
            SELECT id, name, created_at
            FROM projects
            ORDER BY created_at DESC, id ASC
        """
        async with self._pgsql_client.connection() as conn:
            projects: List[ProjectEntity] = []
            for row in await conn.fetch(query):
                projects.append({
                    "id": row["id"],
                    "name": row["name"],
                    "created_at": row["created_at"],
                })
            return projects
