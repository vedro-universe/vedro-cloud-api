from datetime import datetime
from typing import List, TypedDict

from .repository import Repository
from ..clients import MongoClient

__all__ = ("ProjectRepository", "ProjectEntity",)


class ProjectEntity(TypedDict):
    id: str
    name: str
    created_at: datetime


class ProjectRepository(Repository):
    def __init__(self, mongo_client: MongoClient) -> None:
        self._mongo_client = mongo_client

    async def get_projects(self) -> List[ProjectEntity]:
        projects: List[ProjectEntity] = []

        async with self._mongo_client as db:
            async for record in db["projects"].find():
                projects.append({
                    "id": record["id"],
                    "name": record["name"],
                    "created_at": record["created_at"],
                })
        return projects
