from cabina import env
from sanic.config import Config as SanicConfig

__all__ = ("Config",)


class Config(SanicConfig):
    APP_HOST = env.str("VEDRO_CLOUD_HOST", default="0.0.0.0")
    APP_PORT = env.int("VEDRO_CLOUD_PORT", default=80)
