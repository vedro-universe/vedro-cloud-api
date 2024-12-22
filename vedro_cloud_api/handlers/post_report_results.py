from http import HTTPStatus

from sanic import HTTPResponse, Request
from sanic.response import json

from ..models.project import Project

__all__ = ("post_report_results",)


async def post_report_results(request: Request, project_id: str, report_id: str) -> HTTPResponse:
    project = Project(id=project_id)
    await request.app.ctx.project_repo.create(project)

    return json({}, status=HTTPStatus.ACCEPTED)
