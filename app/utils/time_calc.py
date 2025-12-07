from datetime import datetime
from typing import List, Optional


def avg_wait_time(durations: List[float]) -> Optional[float]:
    if not durations:
        return None
    return sum(durations) / len(durations)


def duration_seconds(start: datetime, end: Optional[datetime]) -> Optional[float]:
    if not end:
        return None
    return (end - start).total_seconds()
