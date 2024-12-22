from sanic import HTTPResponse, Request
from sanic.response import json

__all__ = ("get_projects",)


async def get_projects(request: Request) -> HTTPResponse:
    return json({
        "total": 0,
        "projects": [],
    })
