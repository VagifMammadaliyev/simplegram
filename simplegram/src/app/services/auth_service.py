import datetime
from typing import Optional

from fastapi_jwt_auth import AuthJWT

from app.core.settings import get_settings
from app.schemas.user_schemas import UserRecordSchema
from app.schemas.auth_schemas import RegisterRequestSchema, LoginRequestSchema
from app.repositories.users_repository import UsersRepository
from app.utils.crypto import PasswordHasher
from app.errors.database_errors import DuplicateKeyError
from app.errors.app_errors import ValidationError, LoginError


app_settings = get_settings()


class AuthService:
    def __init__(
        self,
        users_repository: Optional[UsersRepository] = None,
        password_hasher: Optional[PasswordHasher] = None,
        login_token_handler: Optional[AuthJWT] = None,
    ) -> None:
        self.users_repository = users_repository
        self.password_hasher = password_hasher
        self.login_token_handler = login_token_handler

    async def register(self, register_data: RegisterRequestSchema) -> UserRecordSchema:
        user = UserRecordSchema(
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            email=register_data.email,
            hashed_password=self.password_hasher.get_hash(register_data.password),
        )
        try:
            await self.users_repository.create(user)
        except DuplicateKeyError as error:
            raise ValidationError(
                error_data=[
                    {"field": error.duplicate_key_name, "detail": "already exists"}
                ]
            )
        return user

    async def login(self, login_data: LoginRequestSchema) -> str:
        user = await self.users_repository.get_by_email(login_data.email)
        if not user or not self.password_hasher.verify_password(
            login_data.password, user.hashed_password
        ):
            raise LoginError
        await self.users_repository.update_last_login(
            user.id, datetime.datetime.utcnow()
        )
        return (
            self.login_token_handler.create_access_token(subject=str(user.id)),
            self.login_token_handler.create_refresh_token(subject=str(user.id)),
        )

    async def refresh_token(self) -> str:
        self.login_token_handler.jwt_refresh_token_required()
        current_subjet = self.login_token_handler.get_jwt_subject()
        return self.login_token_handler.create_access_token(subject=current_subjet)
