from aiohttp import web
from aiohttp.web import Application

from .clients import PgsqlClient
from .config import Config
from .handlers import get_scenarios, healthcheck, post_history
from .repositories import HistoryRepository

__all__ = ("create_app",)


async def create_app() -> Application:
    app = Application()

    pgsql_client = PgsqlClient(Config.Database.DSN)
    app["history_repo"] = HistoryRepository(pgsql_client)

    app.add_routes([
        web.get("/healthcheck", healthcheck),
        web.post("/v0.2/projects/{project_id}/history", post_history),
        web.get("/v0.2/projects/{project_id}/scenarios", get_scenarios),
    ])

    return app
