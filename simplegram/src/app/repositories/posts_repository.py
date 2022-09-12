import uuid
from typing import List

from app.schemas.post_schemas import (
    PostRecordSchema,
    PostActionRecordSchema,
    PostAction,
)
from app.repositories.base import Repository


class PostsRepository(Repository):
    async def create(self, post: PostRecordSchema) -> PostRecordSchema:
        return await self._create(post)

    async def list(self) -> List[PostRecordSchema]:
        post_results = await self._list()
        return [PostRecordSchema(**post) for post in post_results]

    async def get(self, post_id: uuid.UUID) -> PostRecordSchema:
        result = await self._get({"_id": post_id})
        return PostRecordSchema(**result)

    async def change_like_count(
        self, post_id: uuid.UUID, like_count_delta: int
    ) -> None:
        await self._update_one(
            {"_id": post_id},
            {"$inc": {"like_count": like_count_delta}},
        )


class PostActionsRepository(Repository):
    COLLECTION = "post_actions"

    async def create(
        self, post_action: PostActionRecordSchema
    ) -> PostActionRecordSchema:
        return await self._create(post_action)

    async def delete_by_action(self, post_id: uuid.UUID, action: PostAction) -> int:
        result = await self._delete({"post_id": post_id, "action": action.value})
        return result.deleted_count
