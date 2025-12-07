from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import stats_service

router = APIRouter()


@router.get("/queue/{queue_id}")
def queue_stats(queue_id: int, db: Session = Depends(get_db)):
    s = stats_service.compute_queue_stats(db, queue_id)
    if s is None:
        raise HTTPException(status_code=404, detail="Queue not found or no data")
    return s
