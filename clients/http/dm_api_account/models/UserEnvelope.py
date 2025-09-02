from datetime import datetime
from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, ConfigDict, Field


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class User(BaseModel):
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


class UserEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    resource: User
    metadata: Dict[str, str] | None = None
