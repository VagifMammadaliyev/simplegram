from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from app.services.auth_service import AuthService
from app.repositories.users_repository import UsersRepository
from app.utils.crypto import PasswordHasher


def auth_service(
    users_repository: UsersRepository = Depends(), jwt_auth: AuthJWT = Depends()
) -> AuthService:
    password_hasher = PasswordHasher()
    return AuthService(
        users_repository=users_repository,
        password_hasher=password_hasher,
        login_token_handler=jwt_auth,
    )
