from sanic import HTTPResponse, Request
from sanic.response import json

__all__ = ("get_project_reports",)


async def get_project_reports(request: Request, project_id: str) -> HTTPResponse:
    return json({
        "total": 0,
        "reports": [],
    })
