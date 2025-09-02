from pydantic import BaseModel, ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str
    password: str
    email: str
