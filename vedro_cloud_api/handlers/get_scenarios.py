from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

from ..repositories import HistoryRepository
from ..utils import validate_project_id

__all__ = ("get_scenarios",)


async def get_scenarios(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    project_id = request.match_info["project_id"]
    assert validate_project_id(project_id)

    order_by = request.query.getone("order_by")
    scenarios = await history_repo.get_scenarios(project_id, order_by=order_by)

    return json_response(scenarios, status=HTTPStatus.OK)
