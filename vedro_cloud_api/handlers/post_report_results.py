from http import HTTPStatus

from pydantic import ValidationError
from sanic import HTTPResponse, Request
from sanic.response import json

from ..models.launch import Launch
from ..models.project import Project
from ..models.report import Report

__all__ = ("post_report_results",)


async def post_report_results(request: Request, project_id: str, report_id: str) -> HTTPResponse:
    project = Project(id=project_id)
    await request.app.ctx.project_repo.create(project)

    report = Report(id=report_id, project_id=project.id)
    await request.app.ctx.report_repo.create(report)

    try:
        launch = Launch(**request.json, report_id=report.id)
    except ValidationError as e:
        return json({"errors": e.errors()}, status=HTTPStatus.BAD_REQUEST)
    await request.app.ctx.launch_repo.create(launch)

    for scenario_result in launch.scenario_results:
        await request.app.ctx.scenario_result_repo.create(scenario_result, launch.id)

    return json({}, status=HTTPStatus.ACCEPTED)
