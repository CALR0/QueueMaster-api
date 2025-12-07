from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StatsRead(BaseModel):
    queue_id: int
    metric: str
    value: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
