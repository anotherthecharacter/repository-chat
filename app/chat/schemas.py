from pydantic import BaseModel, UUID4, validator
from typing import Optional
from datetime import datetime


class User(BaseModel):
    id: UUID4
    username: str
    photo_url: Optional[str]


class Chat(BaseModel):
    id: int
    name: str
    status: int
    updated_at: int


    @validator("status")
    def validate_status(cls, value):
        if value not in (0, 1):
            raise ValueError("Invalid status value. Must be 0 or 1.")

        return value


class UserChat(BaseModel):
    id: int
    user_id: UUID4
    chat_id: int


class UserMessage(BaseModel):
    id: int
    sender_id: UUID4
    receiver_id: UUID4
    text: str
    time_delivered: datetime
    time_seen: Optional[datetime]
    is_delivered: bool
