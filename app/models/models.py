"""SQLAlchemy models: Queue, Ticket, Stats.

This file defines three core models. Keep them simple for the example.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class TicketStatus(str, enum.Enum):
    waiting = "waiting"
    served = "served"
    cancelled = "cancelled"


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="queue", cascade="all, delete-orphan")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True, nullable=False)
    queue_id = Column(Integer, ForeignKey("queues.id"), nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.waiting)
    created_at = Column(DateTime, default=datetime.utcnow)
    served_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)

    queue = relationship("Queue", back_populates="tickets")


class Stats(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    queue_id = Column(Integer, ForeignKey("queues.id"), nullable=False)
    metric = Column(String, nullable=False)
    value = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
