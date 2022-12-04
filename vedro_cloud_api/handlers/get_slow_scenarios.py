from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

from ..repositories import HistoryRepository

__all__ = ("get_slow_scenarios",)


async def get_slow_scenarios(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    scenarios = await history_repo.get_slow_scenarios()

    return json_response(scenarios, status=HTTPStatus.OK)
