import datetime
import uuid

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from app.core.settings import get_settings
from app.repositories.users_repository import UsersRepository
from app.schemas.user_schemas import UserRecordSchema

app_settings = get_settings()


async def get_current_user(
    Authorize: AuthJWT = Depends(), users_repository: UsersRepository = Depends()
) -> UserRecordSchema:
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    user = await users_repository.get(uuid.UUID(user_id))
    if user:
        await users_repository.update_last_request(user.id, datetime.datetime.utcnow())
    return user
