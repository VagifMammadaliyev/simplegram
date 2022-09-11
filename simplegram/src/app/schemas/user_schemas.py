from pydantic import *

from app.schemas.base import StorageSchema, JsonSchema


class UserRecordSchema(StorageSchema):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class UserResponseSchema(JsonSchema):
    first_name: str
    last_name: str
    email: EmailStr
