import cabina
from cabina import env


class Config(cabina.Config):
    class App(cabina.Section):
        HOST: str = env.str("HOST", "0.0.0.0")
        PORT: int = env.int("PORT", default=80)

    class Database(cabina.Section):
        URI: str = env.str("DB_URI")
        NAME: str = env.str("DB_NAME", "vedro_cloud")
