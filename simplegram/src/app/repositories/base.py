from typing import Any, TypeVar, Dict, Any

from fastapi import Depends

from app.core.database import Engine
from app.schemas.base import StorageSchema
from app.dependencies import database


Record = TypeVar("Record", bound=StorageSchema)


class Repository:
    def __init__(self, database_engine: Engine = Depends(database)) -> None:
        self.database = database_engine

    @property
    def collection(self) -> str:
        return getattr(
            self,
            "COLLECTION",
            self.__class__.__name__.lower().replace("repository", ""),
        )

    async def _create(self, instance: Record) -> Any:
        result = await self.database.insert(self.collection, instance.dict())
        return result.inserted_id

    async def _get(self, criteria: Dict[str, Any]) -> Any:
        return await self.database.find_one(self.collection, criteria)
