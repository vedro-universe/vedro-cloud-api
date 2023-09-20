from types import TracebackType
from typing import Type

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase as MotorDatabase

__all__ = ("MongoClient",)


class MongoClient:
    def __init__(self, uri: str, db_name: str) -> None:
        self._uri = uri
        self._db_name = db_name
        self._client: MotorClient | None = None

    async def __aenter__(self) -> MotorDatabase:
        self._client = MotorClient(self._uri)
        return self._client[self._db_name]

    async def __aexit__(self,
                        exc_type: Type[BaseException] | None,
                        exc_value: BaseException | None,
                        traceback: TracebackType | None) -> None:
        if self._client:
            self._client.close()
