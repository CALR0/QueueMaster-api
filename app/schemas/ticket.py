from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.models import TicketStatus


class TicketCreate(BaseModel):
    queue_id: int


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus]


class TicketRead(BaseModel):
    id: int
    number: int
    queue_id: int
    status: TicketStatus
    created_at: datetime
    served_at: Optional[datetime]

    class Config:
        orm_mode = True
