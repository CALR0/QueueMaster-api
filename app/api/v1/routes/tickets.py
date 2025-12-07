from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.services import ticket_service
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.models.models import TicketStatus

router = APIRouter()


@router.post("/", response_model=TicketRead)
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    try:
        t = ticket_service.create_ticket(db, ticket_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return t


@router.post("/assign/{queue_id}", response_model=TicketRead)
def assign_next(queue_id: int, db: Session = Depends(get_db)):
    t = ticket_service.assign_next(db, queue_id)
    if not t:
        raise HTTPException(status_code=404, detail="No tickets to assign")
    return t


@router.patch("/{ticket_id}", response_model=TicketRead)
def change_status(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    status = payload.status
    if not status:
        raise HTTPException(status_code=400, detail="No status provided")
    t = ticket_service.change_status(db, ticket_id, status)
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t


@router.get("/queue/{queue_id}", response_model=List[TicketRead])
def list_by_queue(queue_id: int, db: Session = Depends(get_db)):
    return ticket_service.list_tickets(db, queue_id)
