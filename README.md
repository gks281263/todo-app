# Todo App

Simple todo app. FastAPI backend, React frontend, SQLite for storage.

## Setup

Easiest way:

```bash
./run.sh
```

That handles the venv, dependencies, migrations, and starts both servers.

Or do it manually:

```bash
# backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Backend runs on :8000, frontend on :5173. API docs at /docs.

## API

```
GET    /api/todos          list (paginated, filterable)
POST   /api/todos          create
GET    /api/todos/:id      get one
PATCH  /api/todos/:id      partial update
DELETE /api/todos/:id      delete
GET    /api/health         health check
```

Listing supports `page`, `page_size`, and `status` query params.

## Tests

```bash
cd backend
pytest -v
```

21 tests, runs against SQLite in-memory so no db setup needed. Covers the API endpoints and service layer -- creates, updates, deletes, pagination, filtering, validation errors, 404s.

## How it's structured

```
backend/
  app/
    config.py       pydantic-settings, reads from .env
    database.py     engine, session, get_db dependency
    models.py       Todo model + TodoStatus enum
    schemas.py      pydantic schemas for request/response
    service.py      business logic (queries, creates, etc)
    routes.py       FastAPI endpoints, thin layer over service
    exceptions.py   TodoNotFound + exception handler
    main.py         app setup, cors, middleware
  alembic/          migrations
  tests/            pytest suite
frontend/
  src/
    api.js          fetch wrapper for the backend
    App.jsx         main component, state management
    components/     TodoForm, TodoItem, Pagination
```

Flat structure, intentionally. A single-model CRUD app doesn't need packages within packages.

## Technical notes

**Database**: SQLite locally (just a file, zero setup), but the code works fine with Postgres -- just swap `DATABASE_URL` in `.env`. The model uses `native_enum=False` so the enum maps to a varchar column instead of a native PG enum, which keeps things portable. Indexes on `status` and `due_date` since those are the obvious filter/sort candidates.

**SQLAlchemy 2.0 style**: Using `mapped_column` and `Mapped` type annotations. `DeclarativeBase` instead of the old `declarative_base()` function. Queries use `select()` instead of the legacy `session.query()` API.

**Partial updates**: PATCH with `model_dump(exclude_unset=True)` so clients only send the fields they want to change. The alternative (PUT with full replacement) is more annoying for callers who just want to toggle a status.

**UUIDs**: Primary keys are UUIDs instead of auto-increment integers. Slightly more overhead but avoids leaking info about how many records exist and is generally better practice for anything exposed via API.

**Service layer**: Functions in `service.py` take a db session and do the actual work. Routes are thin -- they parse the request, call a service function, return the response. No repository abstraction; for one model that's just unnecessary indirection.

**Error handling**: `TodoNotFound` exception with a registered handler that returns a proper 404 JSON response. Validation errors go through FastAPI/Pydantic's built-in 422 handling.

**Testing**: Tests override the `get_db` dependency to inject a SQLite in-memory session. Each test gets a fresh database (tables created/dropped per test via an autouse fixture). The API tests use FastAPI's `TestClient`, service tests call the functions directly.

**Frontend**: Minimal React app, no state library, no component library. Just `useState`/`useEffect`/`useCallback` and vanilla CSS. The API client is a thin wrapper around `fetch`. Inline editing, status filtering, pagination, confirm on delete.


## Environment

Copy `.env.example` to `.env`. Only thing you'd change is `DATABASE_URL` if you want to point at Postgres instead of SQLite.
