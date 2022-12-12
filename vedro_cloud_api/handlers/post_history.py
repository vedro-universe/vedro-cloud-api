from datetime import datetime
from http import HTTPStatus
from uuid import UUID, uuid4

from aiohttp.web import Request, Response, json_response
from d42 import schema

from ..repositories import HistoryEntity, HistoryRepository
from ..schemas import HistoryListSchema, ProjectIdSchema
from ..utils import make_hash, validate

__all__ = ("post_history",)

SegmentsSchema = schema.dict({
    "project_id": ProjectIdSchema,
})


async def post_history(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    if errors := validate(request.match_info, SegmentsSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)
    project_id = request.match_info["project_id"]

    payload = await request.json()
    if errors := validate(payload, HistoryListSchema):
        return json_response({"errors": errors}, status=HTTPStatus.BAD_REQUEST)

    history = []
    for record in payload:
        report_id = record["report_id"] if record["report_id"] else str(uuid4())
        entity: HistoryEntity = {
            "id": UUID(record["id"]),
            "launch_id": UUID(record["launch_id"]),
            "report_id": report_id,
            "report_hash": make_hash(report_id),

            "scenario_hash": record["scenario_path"],
            "scenario_path": record["scenario_path"],
            "scenario_subject": record["scenario_subject"],

            "status": record["status"],
            "started_at": datetime.fromtimestamp(record["started_at"] / 1000),
            "ended_at": datetime.fromtimestamp(record["ended_at"] / 1000),
        }
        history.append(entity)

    try:
        await history_repo.save_history_entities(project_id, history)
    except Exception as e:
        print("Error: ", type(e), e)
        return json_response({"errors": ["Internal server error"]},
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return json_response(payload, status=HTTPStatus.OK)
