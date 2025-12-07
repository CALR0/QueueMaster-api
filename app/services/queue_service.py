from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.models import Queue
from app.schemas.queue import QueueCreate, QueueUpdate


def create_queue(db: Session, queue_in: QueueCreate) -> Queue:
    q = Queue(name=queue_in.name, description=queue_in.description)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def get_queue(db: Session, queue_id: int) -> Optional[Queue]:
    return db.query(Queue).filter(Queue.id == queue_id).first()


def list_queues(db: Session, skip: int = 0, limit: int = 100) -> List[Queue]:
    return db.query(Queue).offset(skip).limit(limit).all()


def update_queue(db: Session, queue_id: int, q_in: QueueUpdate) -> Optional[Queue]:
    q = get_queue(db, queue_id)
    if not q:
        return None
    if q_in.name is not None:
        q.name = q_in.name
    if q_in.description is not None:
        q.description = q_in.description
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def delete_queue(db: Session, queue_id: int) -> bool:
    q = get_queue(db, queue_id)
    if not q:
        return False
    db.delete(q)
    db.commit()
    return True
