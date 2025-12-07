from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class StatsRead(BaseModel):
    queue_id: int
    metric: str
    value: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
