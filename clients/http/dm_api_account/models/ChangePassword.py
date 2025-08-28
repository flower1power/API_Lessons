from pydantic import BaseModel, ConfigDict, Field


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    login: str
    token: str
    old_password: str = Field(..., alias="oldPassword")
    new_password: str = Field(..., alias="newPassword")
