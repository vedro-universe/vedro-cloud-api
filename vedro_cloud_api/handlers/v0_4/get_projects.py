import string
from datetime import datetime
from http import HTTPStatus
from random import choice, randint

from aiohttp.web import Request, Response, json_response
from aiohttp_valera_validator import validate

from ...repositories import ProjectRepository
from ...schemas import EmptyParamsSchema
from ...utils import format_datetime

__all__ = ("get_projects",)


@validate(params=EmptyParamsSchema)
async def get_projects(request: Request) -> Response:
    project_repo: ProjectRepository = request.app["project_repo"]

    projects = await project_repo.get_projects()
    result = []
    for project in projects:
        result.append({
            "id": project["id"],
            "name": project["name"],
            "created_at": format_datetime(project["created_at"]),
            "last_report": {
                "id": "".join(choice(string.ascii_lowercase + string.digits) for _ in range(8)),
                "status": choice(["passed", "failed"]),
                "started_at": format_datetime(datetime.utcnow()),
                "total": randint(0, 100),
                "passed": randint(0, 100),
                "failed": randint(0, 100),
                "skipped": randint(0, 100),
            }
        })

    return json_response(status=HTTPStatus.OK, data={
        "total": len(result),
        "items": result,
    })
