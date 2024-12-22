from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from asyncpg.connection import Connection
from asyncpg.pool import Pool

__all__ = ("PostgreSQL",)


class PostgreSQL:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._pool: Pool | None = None

    async def create_pool(self) -> None:
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self.dsn)

    async def close_pool(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[Connection, None]:
        assert self._pool is not None  # for type checker
        conn = await self._pool.acquire()
        try:
            yield conn
        finally:
            await self._pool.release(conn)
