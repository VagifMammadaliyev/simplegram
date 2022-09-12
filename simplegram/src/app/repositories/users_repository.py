import uuid
import datetime
from typing import Optional

from app.repositories.base import Repository
from app.schemas.user_schemas import UserRecordSchema


class UsersRepository(Repository):
    async def create(self, user: UserRecordSchema) -> UserRecordSchema:
        return await self._create(user)

    async def get_by_email(self, email: str) -> Optional[UserRecordSchema]:
        result = await self._get({"email": email})
        return UserRecordSchema(**result) if result else None

    async def get(self, user_id: uuid.UUID) -> Optional[UserRecordSchema]:
        result = await self._get({"_id": user_id})
        return UserRecordSchema(**result) if result else None

    async def update_last_login(
        self, user_id: uuid.UUID, last_login: datetime.datetime
    ) -> None:
        await self._update_one(
            {"_id": user_id},
            {"$set": {"last_login": last_login}},
        )

    async def update_last_request(
        self, user_id: uuid.UUID, last_request: datetime.datetime
    ) -> None:
        await self._update_one(
            {"_id": user_id},
            {"$set": {"last_request": last_request}},
        )
