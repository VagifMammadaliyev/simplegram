from fastapi.routing import APIRouter

from app.endpoints import v1

api_router = APIRouter()

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(v1.auth_router)
v1_router.include_router(v1.post_router)

api_router.include_router(v1_router)
