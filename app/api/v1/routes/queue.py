from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db, engine
from app.db.base import Base
from app.services import queue_service
from app.schemas.queue import QueueCreate, QueueRead, QueueUpdate

router = APIRouter()


@router.on_event("startup")
def startup():
    # Create tables for demo purposes. Use Alembic for production migrations.
    Base.metadata.create_all(bind=engine)


@router.post("/", response_model=QueueRead)
def create(q_in: QueueCreate, db: Session = Depends(get_db)):
    q = queue_service.create_queue(db, q_in)
    return q


@router.get("/", response_model=List[QueueRead])
def list_all(db: Session = Depends(get_db)):
    return queue_service.list_queues(db)


@router.get("/{queue_id}", response_model=QueueRead)
def get_queue(queue_id: int, db: Session = Depends(get_db)):
    q = queue_service.get_queue(db, queue_id)
    if not q:
        raise HTTPException(status_code=404, detail="Queue not found")
    return q


@router.put("/{queue_id}", response_model=QueueRead)
def update_queue(queue_id: int, q_in: QueueUpdate, db: Session = Depends(get_db)):
    q = queue_service.update_queue(db, queue_id, q_in)
    if not q:
        raise HTTPException(status_code=404, detail="Queue not found")
    return q


@router.delete("/{queue_id}")
def delete_queue(queue_id: int, db: Session = Depends(get_db)):
    ok = queue_service.delete_queue(db, queue_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Queue not found")
    return {"deleted": True}
