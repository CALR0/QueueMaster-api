from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.db.base import Base


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    queue_id = Column(Integer, ForeignKey("queues.id"), nullable=False)
    metric = Column(String, nullable=False)
    value = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
