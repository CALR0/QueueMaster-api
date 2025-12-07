from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models import TicketStatus


class TicketCreate(BaseModel):
    queue_id: int


class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None


class TicketRead(BaseModel):
    id: int
    number: int
    queue_id: int
    status: TicketStatus
    created_at: datetime
    served_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
