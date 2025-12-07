from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.models.models import Ticket, Queue, TicketStatus
from app.schemas.ticket import TicketCreate
from app.utils.fifo import FIFOQueue
from app.utils.time_calc import duration_seconds

# Simple in-memory map of queue_id -> FIFOQueue for pending ticket numbers
_fifo_queues = {}


def _get_fifo(queue_id: int) -> FIFOQueue:
    if queue_id not in _fifo_queues:
        _fifo_queues[queue_id] = FIFOQueue()
    return _fifo_queues[queue_id]


def create_ticket(db: Session, ticket_in: TicketCreate) -> Ticket:
    # Determine next ticket number for this queue
    q = db.query(Queue).filter(Queue.id == ticket_in.queue_id).first()
    if not q:
        raise ValueError("Queue not found")

    last = db.query(Ticket).filter(Ticket.queue_id == q.id).order_by(Ticket.number.desc()).first()
    next_number = 1 if not last else last.number + 1
    ticket = Ticket(number=next_number, queue_id=q.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Push to in-memory FIFO for quick assignment
    fifo = _get_fifo(q.id)
    fifo.push(ticket.id)
    return ticket


def assign_next(db: Session, queue_id: int) -> Optional[Ticket]:
    fifo = _get_fifo(queue_id)
    next_ticket_id = fifo.pop()
    if not next_ticket_id:
        return None
    ticket = db.query(Ticket).filter(Ticket.id == next_ticket_id).first()
    if not ticket:
        return None
    ticket.status = TicketStatus.served
    ticket.served_at = datetime.utcnow()
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def change_status(db: Session, ticket_id: int, status: TicketStatus) -> Optional[Ticket]:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return None
    ticket.status = status
    if status == TicketStatus.served:
        ticket.served_at = datetime.utcnow()
    if status == TicketStatus.cancelled:
        ticket.canceled_at = datetime.utcnow()
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def list_tickets(db: Session, queue_id: int) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.queue_id == queue_id).order_by(Ticket.number.asc()).all()
