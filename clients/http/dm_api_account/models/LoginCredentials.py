from pydantic import BaseModel, ConfigDict, Field


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    login: str
    password: str
    remember_me: bool | None = Field(True, alias="rememberMe")
