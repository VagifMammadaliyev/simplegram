from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from app.repositories.posts_repository import PostActionsRepository, PostsRepository
from app.repositories.users_repository import UsersRepository
from app.services.auth_service import AuthService
from app.services.post_service import PostService
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


def post_service(
    posts_repository: PostsRepository = Depends(),
    post_actions_repository: PostActionsRepository = Depends(),
) -> PostService:
    return PostService(
        posts_repository=posts_repository,
        post_actions_repository=post_actions_repository,
    )
