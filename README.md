# Todo App

A straightforward Todo application built with FastAPI, PostgreSQL, and React.

## Prerequisites

- Python 3.11+
- Node.js 18+

## Quick Start

The easiest way -- run everything with one script:

```bash
chmod +x run.sh
./run.sh
```

This sets up a Python venv, installs deps, runs migrations (SQLite), and launches both backend and frontend.

### Manual Setup

If you prefer to run things separately:

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

- Backend: `http://localhost:8000` (docs at `/docs`)
- Frontend: `http://localhost:5173`

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/todos | List todos (paginated, filterable by status) |
| POST | /api/todos | Create a todo |
| GET | /api/todos/:id | Get a todo |
| PATCH | /api/todos/:id | Partial update |
| DELETE | /api/todos/:id | Delete a todo |
| GET | /api/health | Health check |

Query params for listing: `page`, `page_size`, `status` (pending/in_progress/completed).

## Tests

```bash
cd backend
pytest -v
```

Tests use SQLite in-memory, no database setup needed.

## Project Structure

```
backend/
  app/
    main.py          # FastAPI app setup
    config.py        # Settings from env
    database.py      # SQLAlchemy engine + session
    models.py        # Todo model
    schemas.py       # Request/response schemas
    service.py       # Business logic
    routes.py        # API endpoints
    exceptions.py    # Error handling
  alembic/           # Migrations
  tests/
frontend/
  src/
    App.jsx          # Main component
    api.js           # Backend client
    components/      # UI components
```

## Architecture Decisions

**Flat structure** -- No nested packages. A Todo app doesn't need domain-driven design. One service module, one routes module, done.

**Service layer but no repository** -- The service functions talk directly to SQLAlchemy. Adding a repository abstraction for a single model would be ceremony without value.

**UUIDs for IDs** -- Avoids sequential enumeration of resources. Minor overhead but standard practice for APIs.

**SQLite for tests** -- Fast, zero-config. The ORM abstracts away dialect differences for basic CRUD. For a production app with complex queries, you'd want to test against Postgres too.

**PATCH for updates** -- Partial updates via `exclude_unset`. PUT would require sending the full object, which is annoying for clients that just want to flip a status.

**No auth** -- Intentionally omitted. Would add JWT or session-based auth in a real deployment, but it's orthogonal to the core CRUD logic.

## Environment

Copy `.env.example` to `.env` and adjust as needed. The only required variable is `DATABASE_URL`.
