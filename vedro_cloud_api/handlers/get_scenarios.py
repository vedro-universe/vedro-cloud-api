from http import HTTPStatus

from aiohttp.web import Request, Response, json_response
from d42 import schema

from ..repositories import HistoryRepository
from ..schemas import ProjectIdSchema
from ..utils import validate

__all__ = ("get_scenarios",)

SegmentsSchema = schema.dict({
    "project_id": ProjectIdSchema,
})

ParamsSchema = schema.dict({
    "order_by": schema.str("duration"),
})


async def get_scenarios(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    if errors := validate(request.match_info, SegmentsSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)
    project_id = request.match_info["project_id"]

    if errors := validate(dict(request.query), ParamsSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)
    order_by = request.query.getone("order_by")

    try:
        scenarios = await history_repo.get_scenarios(project_id, order_by=order_by)
    except Exception as e:
        print("Error: ", type(e), e)
        return json_response({"errors": ["Internal server error"]},
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return json_response(scenarios, status=HTTPStatus.OK)
