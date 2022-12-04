import asyncio

from aiohttp import web

from .app import create_app
from .config import Config

if __name__ == "__main__":
    app = asyncio.run(create_app())
    web.run_app(app, host=Config.App.HOST, port=Config.App.PORT)
