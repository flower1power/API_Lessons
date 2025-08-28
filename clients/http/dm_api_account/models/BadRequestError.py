from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field


class BadRequestError(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    message: str
    invalid_properties: Dict[str, List[str]] = Field(..., alias="invalidProperties")
