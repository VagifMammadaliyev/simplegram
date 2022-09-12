import uuid
import datetime
from enum import Enum
from typing import Optional

from pydantic import *

from app.schemas.base import StorageSchema, JsonSchema


class PostAuthorResponseSchema(JsonSchema):
    first_name: str
    last_name: str


class PostRecordSchema(StorageSchema):
    title: str
    content: str
    user_id: uuid.UUID
    author: PostAuthorResponseSchema = None
    like_count: Optional[int] = 0


class PostAction(str, Enum):
    like = "like"
    unlike = "unlike"


class PostActionRecordSchema(StorageSchema):
    user_id: uuid.UUID
    post_id: uuid.UUID
    action: PostAction
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class PostEditRequestSchema(JsonSchema):
    content: str
    title: str


class PostAnalyticsRequestSchema(JsonSchema):
    date_from: datetime.date
    date_to: datetime.date


class PostResponseSchema(PostRecordSchema):
    pass


class PostAnalyticsResponseSchema(JsonSchema):
    date: datetime.date
    count: int
