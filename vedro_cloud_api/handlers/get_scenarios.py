from http import HTTPStatus
from uuid import uuid4

from aiohttp.web import Request, Response, json_response
from d42 import optional, schema

from ..repositories import HistoryRepository
from ..schemas import ProjectIdSchema, ReportIdSchema
from ..utils import validate

__all__ = ("get_scenarios",)

SegmentsSchema = schema.dict({
    "project_id": ProjectIdSchema,
})

ParamsSchema = schema.dict({
    "order_by": schema.str("duration"),
    optional("report_id"): ReportIdSchema,
})


async def get_scenarios(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    if errors := validate(request.match_info, SegmentsSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)
    project_id = request.match_info["project_id"]

    if errors := validate(dict(request.query), ParamsSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)
    order_by = request.query.getone("order_by")
    report_id = request.query.get("report_id", str(uuid4()))

    try:
        scenarios = await history_repo.get_scenarios(project_id, order_by, report_id)
    except Exception as e:
        print("Error: ", type(e), e)
        return json_response({"errors": ["Internal server error"]},
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return json_response(scenarios, status=HTTPStatus.OK)
