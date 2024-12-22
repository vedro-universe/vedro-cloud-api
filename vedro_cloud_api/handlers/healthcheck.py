from sanic import HTTPResponse, Request
from sanic.response import json

__all__ = ("healthcheck",)


async def healthcheck(request: Request) -> HTTPResponse:
    return json({"status": "ok"})
