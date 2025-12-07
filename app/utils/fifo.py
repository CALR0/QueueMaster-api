"""FIFO in-memory helper for ticket assignment.

This is a simple FIFO queue class used by services to assign the next ticket.
In production you'd likely use Redis or a persistent queue.
"""
from collections import deque
from typing import Optional


class FIFOQueue:
    def __init__(self):
        self._q = deque()

    def push(self, item):
        self._q.append(item)

    def pop(self):
        if self._q:
            return self._q.popleft()
        return None

    def peek(self):
        return self._q[0] if self._q else None

    def __len__(self):
        return len(self._q)
