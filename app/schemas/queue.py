from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class QueueBase(BaseModel):
    name: str
    description: Optional[str] = None


class QueueCreate(QueueBase):
    pass


class QueueUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class QueueRead(QueueBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
