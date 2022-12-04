from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asyncpg import Connection, connect

__all__ = ("PgsqlClient",)


class PgsqlClient:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[Connection, None]:
        conn = await connect(self._dsn)
        try:
            yield conn
        finally:
            await conn.close()
