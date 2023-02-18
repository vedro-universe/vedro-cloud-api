from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate

from ...repositories import TokenRepository
from ...schemas import EmptyParamsSchema
from ...utils import format_datetime

__all__ = ("get_tokens",)


@validate(params=EmptyParamsSchema)
async def get_tokens(request: Request) -> Response:
    token_repo: TokenRepository = request.app["token_repo"]

    tokens = await token_repo.get_tokens()
    result = []
    for token in tokens:
        prefix = str(token["token"])[:8]
        result.append({
            "token": f"{prefix}-****-****-****-************",
            "description": token["description"],
            "created_at": format_datetime(token["created_at"]),
        })

    return json_response(status=HTTPStatus.OK, data={
        "total": len(result),
        "items": result,
    })
