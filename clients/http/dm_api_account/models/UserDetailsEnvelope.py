from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from clients.http.dm_api_account.models.UserEnvelope import UserRole, Rating


class BbParseMode(str, Enum):
    COMMON = "Common"
    INFO = "Info"
    POST = "Post"
    CHAT = "Chat"


class InfoBbText(BaseModel):
    value: str | None = None
    parseMode: BbParseMode


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias="postsPerPage")
    commentsPerPage: int
    topicsPerPage: int
    messagesPerPage: int
    entitiesPerPage: int


class UserSettings(BaseModel):
    colorSchema: ColorSchema
    nannyGreetingsMessage: str | None = None
    paging: PagingSettings


class UserDetails(BaseModel):
    login: str | None = None
    roles: List[UserRole]
    medium_picture_url: str | None = Field(None, alias="mediumPictureUrl")
    small_picture_url: str | None = Field(None, alias="smallPictureUrl")
    status: str | None = None
    rating: Rating
    online: datetime | None = None
    name: str | None = None
    location: str | None = None
    registration: datetime | None = None
    icq: str | None = None
    skype: str | None = None
    original_picture_url: str | None = Field(None, alias="originalPictureUrl")
    info: str
    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    resource: UserDetails
    metadata: str | None = None
