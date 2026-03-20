# SwiftLink - Claude Code Guidelines

## Project Overview

SwiftLink is a URL shortener with a FastAPI backend and a single-page dark-themed frontend. It uses SQLite via SQLAlchemy for persistence and runs in Docker.

## Project Structure

```
app/
  main.py          - FastAPI app, all route definitions, static file serving
  database.py      - SQLAlchemy engine, session, Base
  models.py        - SQLAlchemy ORM models (Link)
  schemas.py       - Pydantic request/response schemas
  crud.py          - Database operations (create, read, update)
  static/
    index.html     - Single-page frontend (HTML/CSS/JS, no build step)
tests/
  test_api.py      - API tests using TestClient with SQLite test DB
```

## Key Patterns

- All endpoints are defined in `app/main.py` — no routers/blueprints
- The `/{code}` catch-all route must remain last before the static mount
- The `GET /` route serves `index.html` via `FileResponse`
- `StaticFiles` is mounted at `/static` after all route definitions
- Frontend uses `window.location.origin` as API base (no hardcoded URLs)
- Short codes are 6 alphanumeric characters

## Commands

- **Run server**: `uvicorn app.main:app --reload`
- **Run tests**: `pytest -v`
- **Lint**: `ruff check .`
- **Docker**: `docker compose up --build`

## CI/CD

GitHub Actions workflow at `.github/workflows/ci.yml`:
1. **lint** — ruff check
2. **test** — pytest (depends on lint)
3. **docker-build** — docker build (depends on test)

Triggers on push/PR to `main` and `dev` branches.

## Branch Strategy

- `main` — production-ready code
- `dev` — development/feature work
