import uuid
import datetime
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

    async def delete_by_action(
        self, user_id: uuid.UUID, post_id: uuid.UUID, action: PostAction
    ) -> int:
        result = await self._delete(
            {"post_id": post_id, "user_id": user_id, "action": action.value}
        )
        return result.deleted_count

    async def get_analytics(self, date_from: datetime.date, date_to: datetime.date):
        pipeline = [
            {
                "$match": {
                    "action": PostAction.like.value,
                    "timestamp": {
                        "$gte": datetime.datetime.fromisoformat(date_from.isoformat()),
                        "$lte": datetime.datetime.fromisoformat(date_to.isoformat()),
                    },
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$timestamp",
                        },
                    },
                    "count": {"$sum": 1},
                    "first": {"$min": "$timestamp"},
                },
            },
            {"$sort": {"_id.date": 1}},
            {
                "$project": {
                    "_id": 0,
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$first",
                        }
                    },
                    "count": 1,
                }
            },
        ]
        return await self._aggregate(pipeline)
