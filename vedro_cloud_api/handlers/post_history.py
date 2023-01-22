from datetime import datetime
from http import HTTPStatus
from uuid import UUID, uuid4

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate
from d42 import schema

from ..repositories import HistoryEntity, HistoryRepository
from ..schemas import HistoryListSchema, ProjectIdSchema

__all__ = ("post_history",)

SegmentsSchema = schema.dict({
    "project_id": ProjectIdSchema,
})


@validate(segments=SegmentsSchema, json=HistoryListSchema)
async def post_history(request: Request) -> Response:
    history_repo: HistoryRepository = request.app["history_repo"]

    project_id = request.match_info["project_id"]
    payload = await request.json()

    report_id = str(uuid4())
    if (len(payload) > 0) and (payload[0]["report_id"] is not None):
        report_id = payload[0]["report_id"]

    history = []
    for record in payload:
        entity: HistoryEntity = {
            "id": UUID(record["id"]),
            "launch_id": UUID(record["launch_id"]),
            "report_id": report_id,
            "project_id": project_id,

            "scenario_hash": record["scenario_hash"],
            "scenario_rel_path": record["scenario_rel_path"],
            "scenario_subject": record["scenario_subject"],
            "scenario_namespace": record["scenario_namespace"],

            "status": record["status"],
            "started_at": datetime.fromtimestamp(record["started_at"] / 1000),
            "ended_at": datetime.fromtimestamp(record["ended_at"] / 1000),
        }
        history.append(entity)

    try:
        await history_repo.save_history_entities(project_id, report_id, history)
    except Exception as e:
        print("Error: ", type(e), e)
        return json_response({"errors": ["Internal server error"]},
                             status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return json_response(payload, status=HTTPStatus.OK)
