# QueueMaster

QueueMaster is a backend-only API for managing virtual queues and service tickets
for businesses. It allows creating and managing queues, issuing and assigning
tickets (FIFO), changing ticket states, simulating notifications, and fetching
basic statistics.

Documentation contents
- Feature summary
- Project structure
- Available endpoints (with examples)
- Configuration / Environment variables
- Installation and running (Windows / Unix)
- Tests
- Migrations and deployment
- Troubleshooting

Feature summary
- Queue CRUD (create, list, update, delete).
- Issue tickets per queue (sequential numbers per queue).
- FIFO assignment: pull the next pending ticket.
- Ticket states: `waiting`, `served`, `cancelled`.
- Simulated notifications (mock) for clients.
- Basic statistics: average wait time, min/max, tickets served.

Project structure

- `app/` - main package
	- `__init__.py` - FastAPI instance and lifespan (startup/shutdown)
	- `api/v1/routes/` - REST routes: `queue.py`, `tickets.py`, `stats.py`, `notifications.py`
	- `models/` - SQLAlchemy models split by file: `queue.py`, `ticket.py`, `stats.py`
	- `schemas/` - Pydantic schemas for validation and serialization
	- `services/` - business logic (queues, tickets, stats, notifications)
	- `utils/` - utilities (in-memory FIFO, time calculations, mocks)
	- `db/` - `session.py`, `base.py`, `migrations/` (Alembic placeholder)
	- `core/` - configuration and logging
- `tests/` - tests using `pytest` and FastAPI `TestClient`
- `requirements.txt`, `.env.example`, `README.md`

Endpoints (API v1)

Base URL: `/api/v1`

Queues
- `POST /api/v1/queues/` — Create a new queue
	- JSON body: `{ "name": "My Queue", "description": "Description" }`
	- Response: `QueueRead` (id, name, description, created_at)

- `GET /api/v1/queues/` — List queues

- `GET /api/v1/queues/{queue_id}` — Get a specific queue

- `PUT /api/v1/queues/{queue_id}` — Update a queue (partial)
	- Example body: `{ "description": "New description" }`

- `DELETE /api/v1/queues/{queue_id}` — Delete a queue

Tickets
- `POST /api/v1/tickets/` — Create a ticket
	- Body: `{ "queue_id": 1 }`
	- Response: `TicketRead` (id, number, queue_id, status, created_at)

- `POST /api/v1/tickets/assign/{queue_id}` — Assign (pop) the next FIFO ticket

- `PATCH /api/v1/tickets/{ticket_id}` — Change a ticket's state
	- Body: `{ "status": "served" }` (valid values: `waiting`, `served`, `cancelled`)

- `GET /api/v1/tickets/queue/{queue_id}` — List tickets for a queue

Stats
- `GET /api/v1/stats/queue/{queue_id}` — Simple queue statistics
	- Response: average/min/max (seconds), total tickets and served count

Notifications
- `POST /api/v1/notifications/send` — Send a simulated notification
	- Body: `{ "to": "user@example.com", "subject": "Hello", "message": "Your turn..." }`

Quick examples (curl / PowerShell)

Create queue (curl):

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/queues/ \
	-H "Content-Type: application/json" \
	-d '{"name":"Store A","description":"General service"}'
```

Create ticket (PowerShell):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/tickets/ -Body (ConvertTo-Json @{ queue_id = 1 }) -ContentType 'application/json'
```

Assign next (curl):

```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/tickets/assign/1
```

Configuration / Environment variables

Copy `.env.example` to `.env` and adjust values to your environment. Important variables:

- `DATABASE_URL` — SQLAlchemy URL (default `sqlite:///./queuemaster.db`)
- `SECRET_KEY` — secret key if you add authentication
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token expiration (optional)
- `API_KEY` — example API key for protected endpoints (optional)
- `LOG_LEVEL` — logging level

Installation and running

We recommend using a virtual environment. Examples for different platforms follow.

Unix / macOS / WSL / Git Bash:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app:app --reload
```

Windows PowerShell (recommended; avoids policy issues):

```powershell
# create venv
python -m venv .venv

# install dependencies using the venv's python (activation not required)
.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python -m uvicorn app:app --reload
```

Windows CMD (Command Prompt):

```bat
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python -m uvicorn app:app --reload
```

Interactive docs

After the server is running, the automatic API documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Tests

Tests use `pytest` and an ephemeral SQLite test database. Run:

```bash
.\.venv\Scripts\python -m pytest -q
```

Migrations (Alembic)

The `app/db/migrations/` folder is a placeholder. To use Alembic in production:

```bash
pip install alembic
alembic init app/db/migrations
# then configure alembic.ini/env.py to use your SQLAlchemy connection
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

Troubleshooting

- `ModuleNotFoundError: No module named 'app'` when running `pytest`: run `pytest` from the project root or use the venv's `python`.
- Installation issues on Windows (building native packages): recreate the venv, upgrade `pip setuptools wheel`, and use `--prefer-binary` if needed. This repo pins `PyYAML` to avoid builds on Windows.
- PowerShell blocks `Activate.ps1`: use the venv's `python` directly (`.venv\Scripts\python -m ...`) or temporarily run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`.

Contributing

Pull requests and issues are welcome. For large changes, open an issue describing the intent first.