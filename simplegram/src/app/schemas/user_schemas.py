import datetime
from typing import Optional

from pydantic import *

from app.schemas.base import StorageSchema, JsonSchema


class UserRecordSchema(StorageSchema):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    last_login: Optional[datetime.datetime] = None
    last_request: Optional[datetime.datetime] = None


class UserResponseSchema(JsonSchema):
    first_name: str
    last_name: str
    email: EmailStr
    last_login: Optional[datetime.datetime] = None
    last_request: Optional[datetime.datetime] = None
