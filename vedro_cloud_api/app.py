from aiohttp import web
from aiohttp.web import Application
from aiohttp_cors import ResourceOptions
from aiohttp_cors import setup as setup_cors

from .clients import PgsqlClient
from .config import Config
from .handlers import healthcheck
from .handlers.v0_3 import get_scenarios as v0_3_get_scenarios
from .handlers.v0_3 import post_history as v0_3_post_history
from .handlers.v0_4 import get_projects, get_tokens, post_token
from .repositories import ProjectRepository, TokenRepository

__all__ = ("create_app",)


async def create_app() -> Application:
    app = Application()

    pgsql_client = PgsqlClient(Config.Database.DSN)
    app["project_repo"] = ProjectRepository(pgsql_client)
    app["token_repo"] = TokenRepository(pgsql_client)

    app.add_routes([
        web.get("/healthcheck", healthcheck),

        # v0.3
        web.post("/v0.3/projects/{project_id}/history", v0_3_post_history),
        web.get("/v0.3/projects/{project_id}/scenarios", v0_3_get_scenarios),

        # v0.4
        web.get("/v0.4/projects", get_projects),
        web.get("/v0.4/tokens", get_tokens),
        web.post("/v0.4/tokens", post_token),
    ])

    cors = setup_cors(app, defaults={
        "*": ResourceOptions(allow_methods="*", allow_headers="*")
    })
    for route in list(app.router.routes()):
        cors.add(route)

    return app
