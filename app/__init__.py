"""FastAPI application instance and router registration.

Entry point: `uvicorn app:app --reload` will import this module and expose `app`.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings

from app.api.v1.routes import queue, tickets, stats, notifications
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions: create tables for demo purposes (use Alembic in production)
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown actions (none for now)


app = FastAPI(title="QueueMaster API", version="0.1.0", lifespan=lifespan)

# Basic CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(queue.router, prefix="/api/v1/queues", tags=["queues"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

@app.get("/healthz")
def health():
    return {"status": "ok"}
