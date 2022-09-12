from fastapi import FastAPI
from fastapi.requests import Request
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from pymongo import ASCENDING

from app.core.database import Engine
from app.core.settings import get_settings
from app.errors.app_errors import AppError

app_settings = get_settings()


def _on_application_startup_event(app: FastAPI) -> None:
    async def _initialize_application():
        app.state.settings = app_settings
        app.state.database = Engine(app_settings.MONGO_URL)

        await app.state.database.collection("users").create_index(
            [("email", ASCENDING)], unique=True
        )
        await app.state.database.collection("post_actions").create_index(
            [("user_id", ASCENDING), ("post_id", ASCENDING), ("action", ASCENDING)],
            unique=True,
        )

    return _initialize_application


def _on_application_shutdown_event(app: FastAPI) -> None:
    async def _shutdown_application():
        await app.state.database.close()

    return _shutdown_application


def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.get_status_code(),
        content=exc.get_data(),
    )


def _handle_auth_jwt_exception(request: Request, exc: AuthJWTException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


def initialize_application() -> FastAPI:
    app = FastAPI()
    app.add_event_handler("startup", _on_application_startup_event(app))
    app.add_event_handler("shutdown", _on_application_shutdown_event(app))
    app.add_exception_handler(AppError, _handle_app_error)
    app.add_exception_handler(AuthJWTException, _handle_auth_jwt_exception)
    return app
