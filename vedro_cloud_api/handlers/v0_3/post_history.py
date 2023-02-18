from http import HTTPStatus

from aiohttp.web import Request, Response, json_response

__all__ = ("post_history",)


async def post_history(request: Request) -> Response:
    return json_response([], status=HTTPStatus.OK)
