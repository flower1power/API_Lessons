from pydantic import BaseModel, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str
    password: str
    email: str
