import uuid
from typing import List, Optional

from app.errors.app_errors import ValidationError
from app.errors.database_errors import DuplicateKeyError
from app.repositories.posts_repository import PostActionsRepository, PostsRepository
from app.schemas.post_schemas import (
    PostAction,
    PostActionRecordSchema,
    PostAnalyticsRequestSchema,
    PostAuthorResponseSchema,
    PostEditRequestSchema,
    PostRecordSchema,
    PostResponseSchema,
)
from app.schemas.user_schemas import UserRecordSchema


class PostService:
    def __init__(
        self,
        posts_repository: Optional[PostsRepository] = None,
        post_actions_repository: Optional[PostActionsRepository] = None,
    ) -> None:
        self.posts_repository = posts_repository
        self.post_actions_repository = post_actions_repository

    async def create(
        self, user: UserRecordSchema, post_data: PostEditRequestSchema
    ) -> PostResponseSchema:
        post = PostRecordSchema(
            title=post_data.title,
            content=post_data.content,
            user_id=user.id,
            author=PostAuthorResponseSchema.from_orm(user),
        )
        await self.posts_repository.create(post)
        return PostResponseSchema.from_orm(post)

    async def list(self) -> List[PostResponseSchema]:
        return await self.posts_repository.list()

    async def get(self, post_id: uuid.UUID) -> PostResponseSchema:
        return await self.posts_repository.get(post_id)

    async def make_action(
        self, post_id: uuid.UUID, action: PostAction, user: UserRecordSchema
    ) -> None:
        post_action = PostActionRecordSchema(
            user_id=user.id, post_id=post_id, action=action
        )
        try:
            await self.post_actions_repository.create(post_action)
        except DuplicateKeyError:
            raise ValidationError(
                error_data=[{"field": "post_id", "detail": f"Post already {action}d"}]
            )
        deleted_count = await self.post_actions_repository.delete_by_action(
            user.id,
            post_id,
            action=PostAction.like
            if action == PostAction.unlike
            else PostAction.unlike,
        )
        delta = 1 + deleted_count
        await self.posts_repository.change_like_count(
            post_id, like_count_delta=delta if action == PostAction.like else -delta
        )

    async def get_analytics(self, post_analytics_data: PostAnalyticsRequestSchema):
        return await self.post_actions_repository.get_analytics(
            post_analytics_data.date_from, post_analytics_data.date_to
        )
