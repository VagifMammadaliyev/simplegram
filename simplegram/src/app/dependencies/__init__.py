from fastapi import Request

from app.core.database import Engine


def database(request: Request) -> Engine:
    return request.app.state.database
