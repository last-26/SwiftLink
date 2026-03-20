# SwiftLink - URL Shortener API

A fast and simple URL shortener API built with Python and FastAPI.

## CI/CD Pipeline

```
┌────────┐     ┌────────┐     ┌──────────────┐
│  Lint  │────>│  Test  │────>│ Docker Build │
│ (ruff) │     │(pytest)│     │  (verify)    │
└────────┘     └────────┘     └──────────────┘
```

Triggers on **push** and **pull_request** to `main` and `dev` branches.

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
git clone https://github.com/last-26/SwiftLink.git
cd SwiftLink
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Run tests

```bash
pytest -v
```

### Lint

```bash
ruff check .
```

## API Documentation

Interactive docs available at `http://localhost:8000/docs` when the server is running.

### Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

#### Shorten a URL
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path"}'
# {"short_code":"aB3xYz","short_url":"http://localhost:8000/aB3xYz","original_url":"https://example.com/very/long/path"}
```

#### Redirect
```bash
curl -L http://localhost:8000/aB3xYz
# Redirects (307) to the original URL
```

#### Get Stats
```bash
curl http://localhost:8000/stats/aB3xYz
# {"short_code":"aB3xYz","original_url":"https://example.com/very/long/path","click_count":1,"created_at":"2025-01-01T00:00:00"}
```

## Docker

### Build and run
```bash
docker compose up --build
```

### Build only
```bash
docker build -t swiftlink .
docker run -p 8000:8000 swiftlink
```

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **pytest** - Testing
- **ruff** - Linting
- **Docker** - Containerization
- **GitHub Actions** - CI/CD
