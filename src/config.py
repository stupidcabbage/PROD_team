import os
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
NUMBER_OF_AGENTS = 4


class Env:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

    def get(self, key: str, default: Any = None) -> str:
        value = os.getenv(key, default)
        if not value:
            raise self.ObligatoryValueFromEnvDoesNotExists
        return value

    def get_without_checking(self, key, default) -> str:
        return os.getenv(key, default)

    class ObligatoryValueFromEnvDoesNotExists(Exception):
        def __str__(self):
            return 'Obligatory token does not exists! Check env file.'


class Config:
    def __init__(self):
        self.env = Env()


class DBConfig(Config):
    def __init__(self):
        super().__init__()
        self.url = (
            f'postgresql+asyncpg://{self.env.get("DB_USERNAME")}:{self.env.get("DB_PASSWORD")}@{self.env.get("DB_HOST")}:{self.env.get("DB_PORT")}/{self.env.get("DB_NAME")}')


class JWTConfig(Config):
    def __init__(self):
        super().__init__()
        self.secret_key = self.env.get("SECRET_KEY", "privetmir")


class ExternalAPIConfig(Config):
    def __init__(self):
        super().__init__()
        self.graphhopper_key = self.env.get('GRAPHHOPPER_KEY', 'problems')


db_config = DBConfig()
jwt_config = JWTConfig()
external_api_config = ExternalAPIConfig()
