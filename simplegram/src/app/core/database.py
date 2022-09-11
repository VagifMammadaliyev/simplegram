from re import T
from typing import Dict, Any
from pymongo.results import InsertOneResult
from pymongo.errors import DuplicateKeyError as MongoDuplicateKeyError
from pydantic import AnyUrl
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

from app.errors.database_errors import DuplicateKeyError


class Engine:
    def __init__(self, connection_str: AnyUrl) -> None:
        self.client = AsyncIOMotorClient(str(connection_str))
        self.database_name = connection_str.path.split("/")[-1]
        self.database: AsyncIOMotorDatabase = self.client[self.database_name]

    async def close(self):
        self.client.close()

    def collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.database[collection_name]

    async def insert(
        self, collection_name: str, document: Dict[str, Any]
    ) -> InsertOneResult:
        try:
            return await self.collection(collection_name).insert_one(document)
        except MongoDuplicateKeyError as error:
            key_error_details = error.details.get("keyValue", {})
            key_name = list(key_error_details.keys())[0]
            key_value = key_error_details[key_name]
            raise DuplicateKeyError(
                duplicate_key_name=key_name, duplicate_key_value=key_value
            )

    async def find_one(
        self, collection_name: str, criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        return await self.collection(collection_name).find_one(criteria)