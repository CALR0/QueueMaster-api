from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class QueueBase(BaseModel):
    name: str
    description: Optional[str] = None


class QueueCreate(QueueBase):
    pass


class QueueUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class QueueRead(QueueBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
