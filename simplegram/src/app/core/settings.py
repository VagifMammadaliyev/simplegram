import os
from functools import lru_cache

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings, AnyUrl


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AppSettings(BaseSettings):
    BASE_DIR: str = BASE_DIR

    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    DOCS_URL: str = "/docs"

    MONGO_URL: AnyUrl = ""
    AUTHJWT_SECRET_KEY: str = "secret"
    AUTHJWT_ALGORITHM: str = "HS256"


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()


@AuthJWT.load_config
def get_config():
    return get_settings()
