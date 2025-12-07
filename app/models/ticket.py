from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TicketStatus(str, enum.Enum):
    waiting = "waiting"
    served = "served"
    cancelled = "cancelled"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True, nullable=False)
    queue_id = Column(Integer, ForeignKey("queues.id"), nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.waiting)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    served_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)

    queue = relationship("Queue", back_populates="tickets")
