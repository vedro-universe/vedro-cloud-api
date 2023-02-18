from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

__all__ = ("get_scenarios",)


async def get_scenarios(request: Request) -> Response:
    return json_response([], status=HTTPStatus.OK)
