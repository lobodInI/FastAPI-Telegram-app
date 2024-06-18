from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RequestCreate(BaseModel):
    bot_token: str
    chat_id: str
    message: str


class RequestDetail(BaseModel):
    id: UUID
    bot_token: str
    chat_id: str
    message: str
    response: Optional[dict] = None
    owner_id: UUID

    class Config:
        from_attributes = True
