import cabina
from cabina import env


class Config(cabina.Config):
    class App(cabina.Section):
        HOST: str = env.str("HOST", "0.0.0.0")
        PORT: int = env.int("PORT", default=80)

    class Database(cabina.Section):
        DSN: str = env.str("DB_DSN")
