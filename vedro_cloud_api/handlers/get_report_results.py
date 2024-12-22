from sanic import HTTPResponse, Request
from sanic.response import json

__all__ = ("get_report_results",)


async def get_report_results(request: Request, project_id: str, report_id: str) -> HTTPResponse:
    return json({
        "total": 0,
        "results": [],
    })
