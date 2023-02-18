from datetime import datetime
from typing import List, TypedDict
from uuid import UUID

from ..clients import PgsqlClient
from ..utils import cut_str
from .repository import Repository

__all__ = ("TokenRepository", "TokenEntity",)


class TokenEntity(TypedDict):
    token: UUID
    description: str
    created_at: datetime


class TokenRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    async def create_token(self, token: UUID, description: str, created_at: datetime) -> None:
        query = """
            INSERT INTO tokens (token, description, created_at)
            VALUES ($1, $2, $3)
        """
        async with self._pgsql_client.connection() as conn:
            await conn.execute(query, token, cut_str(description, 255), created_at)

    async def get_tokens(self) -> List[TokenEntity]:
        query = """
            SELECT token, description, created_at
            FROM tokens
            ORDER BY created_at DESC, token ASC
        """
        async with self._pgsql_client.connection() as conn:
            projects: List[TokenEntity] = []
            for row in await conn.fetch(query):
                projects.append({
                    "token": row["token"],
                    "description": row["description"],
                    "created_at": row["created_at"],
                })
            return projects
