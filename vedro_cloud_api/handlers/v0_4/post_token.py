from datetime import datetime
from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate

from ...repositories import TokenRepository
from ...schemas import EmptyParamsSchema, NewTokenSchema
from ...utils import format_datetime

__all__ = ("post_token",)


@validate(params=EmptyParamsSchema, json=NewTokenSchema)
async def post_token(request: Request) -> Response:
    token_repo: TokenRepository = request.app["token_repo"]

    payload = await request.json()
    token = payload["token"]
    description = payload["description"]
    created_at = datetime.utcnow()

    await token_repo.create_token(token, description, created_at)

    result = {
        "token": token,
        "description": description,
        "created_at": format_datetime(created_at),
    }
    return json_response(result, status=HTTPStatus.OK)
