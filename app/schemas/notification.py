from pydantic import BaseModel
from typing import Optional


class NotificationPayload(BaseModel):
    to: str
    subject: str
    message: str
    channel: Optional[str] = "email"
