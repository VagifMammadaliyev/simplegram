import uuid
from typing import Dict, Any

from pydantic import *


class JsonSchema(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {uuid.UUID: str}


class StorageSchema(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        json_encoders = {uuid.UUID: str}

    @root_validator(pre=False)
    def _set_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("_id"):
            values["_id"] = values.get("id")
        return values
