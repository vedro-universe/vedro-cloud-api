from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from aiohttp.web import Request, Response, json_response

from ..entities import HistoryEntity
from ..repositories import HistoryRepository
from ..utils import validate_project_id

__all__ = ("post_history",)


async def post_history(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    project_id = request.match_info["project_id"]
    assert validate_project_id(project_id)

    payload = await request.json()
    history_entities = []
    for x in payload:
        history_entity = HistoryEntity(
            id=UUID(x["id"]),
            scenario_id=x["scenario_id"],
            scenario_hash=x["scenario_hash"],
            scenario_path=x["scenario_path"],
            scenario_subject=x["scenario_subject"],
            status=x["status"],
            started_at=datetime.fromtimestamp(x["started_at"] / 1000),
            ended_at=datetime.fromtimestamp(x["ended_at"] / 1000),
        )
        history_entities.append(history_entity)

    await history_repo.save_history_entities(project_id, history_entities)

    return json_response(payload, status=HTTPStatus.OK)
