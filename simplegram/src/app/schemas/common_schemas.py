from app.schemas.base import JsonSchema


class SimpleDetailResponseSchema(JsonSchema):
    detail: str
