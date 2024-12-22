from types import SimpleNamespace
from typing import Any, Type

from sanic import Sanic

from .clients import PostgreSQL
from .config import Config
from .handlers.get_project_reports import get_project_reports
from .handlers.get_projects import get_projects
from .handlers.get_report_launches import get_report_launches
from .handlers.get_report_results import get_report_results
from .handlers.healthcheck import healthcheck
from .handlers.post_report_results import post_report_results
from .repositories.launch import LaunchRepository
from .repositories.project import ProjectRepository
from .repositories.report import ReportRepository
from .repositories.scenario_result import ScenarioResultRepository

__all__ = ("create_app",)


SanicApp = Sanic[Config, SimpleNamespace]


def create_app(config: Type[Config] = Config) -> SanicApp:
    app = Sanic("VedroCloudAPI", config=config())

    app.add_route(
        get_projects,
        "/v1/projects"
    )
    app.add_route(
        get_project_reports,
        "/v1/projects/<project_id:str>/reports")
    app.add_route(
        get_report_launches,
        "/v1/projects/<project_id:str>/reports/<report_id:str>/launches"
    )
    app.add_route(
        get_report_results,
        "/v1/projects/<project_id:str>/reports/<report_id:str>/results"
    )
    app.add_route(
        post_report_results,
        "/v1/projects/<project_id:str>/reports/<report_id:str>/launches",
        methods={"POST"}
    )

    app.add_route(healthcheck, "/healthcheck")

    async def setup_pgsql(app: SanicApp, *args: Any) -> None:
        await app.ctx.pgsql.create_pool()

        async def close_pgsql(app: SanicApp, *args: Any) -> None:
            await app.ctx.pgsql.close_pool()

        app.register_listener(close_pgsql, "after_server_stop")

    app.register_listener(setup_pgsql, "before_server_start")

    app.ctx.pgsql = PostgreSQL("postgresql://vedro_cloud:vedro_cloud@127.0.0.1:6432/vedro_cloud")
    app.ctx.project_repo = ProjectRepository(app.ctx.pgsql)
    app.ctx.report_repo = ReportRepository(app.ctx.pgsql)
    app.ctx.launch_repo = LaunchRepository(app.ctx.pgsql)
    app.ctx.scenario_result_repo = ScenarioResultRepository(app.ctx.pgsql)

    return app
