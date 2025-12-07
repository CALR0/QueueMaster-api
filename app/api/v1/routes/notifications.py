from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notification import NotificationPayload
from app.services.notification_service import notify_client

router = APIRouter()


@router.post("/send")
def send_notification(payload: NotificationPayload, db: Session = Depends(get_db)):
    # db is unused but kept for parity; in real app you'd store audit logs
    resp = notify_client(payload.to, payload.subject, payload.message, payload.channel)
    if resp.get("status") != "sent":
        raise HTTPException(status_code=500, detail="Failed to send notification")
    return {"ok": True, "detail": resp}
