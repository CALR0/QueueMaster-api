from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any, List

from app.models.models import Ticket, TicketStatus
from app.utils.time_calc import duration_seconds, avg_wait_time


def compute_queue_stats(db: Session, queue_id: int) -> Dict[str, Any]:
    """Compute simple statistics for a queue.

    Returns average/min/max wait time (in seconds), total tickets and served count.
    """
    all_tickets: List[Ticket] = db.query(Ticket).filter(Ticket.queue_id == queue_id).all()

    # compute durations for tickets that have been served
    durations: List[float] = []
    served_count = 0
    for t in all_tickets:
        if t.status == TicketStatus.served:
            served_count += 1
        if t.served_at and t.created_at:
            d = duration_seconds(t.created_at, t.served_at)
            if d is not None:
                durations.append(d)

    stats = {
        "average_wait_seconds": avg_wait_time(durations),
        "min_wait_seconds": min(durations) if durations else None,
        "max_wait_seconds": max(durations) if durations else None,
        "tickets_total": len(all_tickets),
        "tickets_served": served_count,
    }
    return stats
