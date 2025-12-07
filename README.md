# QueueMaster

Backend-only API for managing virtual queues for businesses.

Quick start

1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

Windows (Command Prompt / CMD)

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and adjust values.

3. Run the app:

```powershell
uvicorn app:app --reload
```

Windows (Command Prompt / CMD)

```bat
REM Start the server using the venv's python (no activation required)
.venv\Scripts\python -m uvicorn app:app --reload

REM Or, after activating the venv in CMD:
REM .venv\Scripts\activate.bat
REM uvicorn app:app --reload
```

API

- The application `FastAPI` instance is in `app/__init__.py`.
- Routes are under `app/api/v1/routes/`.

Tests

Run tests with:

```powershell
pytest -q
```

This repository is a minimal, self-contained example of a queue/ticketing backend.

**Robust setup (recommended for Windows users)**

If other users will run this project on Windows, this sequence is the most reliable
and avoids PowerShell execution-policy issues and local build failures (for example
when compiling native wheels).

PowerShell (single-session, no activation required):

```powershell
# remove and recreate a clean virtualenv (optional but recommended when troubleshooting)
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate.bat

# use the venv's python to upgrade pip/wheel/setuptools and install deps
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# run the app
.\.venv\Scripts\python -m uvicorn app:app --reload
```

CMD (Command Prompt) equivalent:

```bat
:: remove and recreate venv
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate.bat

:: install deps and run
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
uvicorn app:app --reload
```

Notes:
- For interactive testing you can open `http://127.0.0.1:8000/docs` after starting the server.