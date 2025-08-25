from pydantic import BaseModel, ConfigDict


class GeneralError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
