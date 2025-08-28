from pydantic import BaseModel, ConfigDict


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str
    email: str
