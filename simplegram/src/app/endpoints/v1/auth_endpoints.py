from fastapi import Depends
from fastapi.routing import APIRouter

from app.dependencies.auth import get_current_user
from app.dependencies.services import auth_service
from app.schemas.auth_schemas import (
    AccessTokenResponseSchema,
    AuthDetailResponseSchema,
    LoginRequestSchema,
    RegisterRequestSchema,
)
from app.schemas.common_schemas import SimpleDetailResponseSchema
from app.schemas.user_schemas import UserRecordSchema, UserResponseSchema
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags={"auth"})


@router.post("/register", response_model=SimpleDetailResponseSchema)
async def register(
    body: RegisterRequestSchema,
    auth_service: AuthService = Depends(auth_service),
) -> SimpleDetailResponseSchema:
    await auth_service.register(body)
    return {"detail": "Registered successfully"}


@router.post("/login", response_model=AuthDetailResponseSchema)
async def login(
    body: LoginRequestSchema,
    auth_service: AuthService = Depends(auth_service),
) -> AuthDetailResponseSchema:
    access_token, refresh_token = await auth_service.login(body)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh_token", response_model=AccessTokenResponseSchema)
async def refresh_token(
    auth_service: AuthService = Depends(auth_service),
) -> AuthDetailResponseSchema:
    access_token = await auth_service.refresh_token()
    return {"access_token": access_token}


@router.get("/me", response_model=UserResponseSchema)
async def me(user: UserRecordSchema = Depends(get_current_user)) -> UserResponseSchema:
    return user
