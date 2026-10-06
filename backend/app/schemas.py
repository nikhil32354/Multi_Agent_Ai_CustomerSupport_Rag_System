from pydantic import BaseModel, ConfigDict
from typing import Optional


class MessageCreate(BaseModel):
    session_id: str
    content: str
    role: str = 'user'


class TicketCreate(BaseModel):
    title: str
    description: Optional[str]


class TicketOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    model_config = ConfigDict(from_attributes=True)
