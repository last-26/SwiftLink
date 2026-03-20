# SwiftLink - URL Shortener

A fast and simple URL shortener with a dark-themed web UI, built with Python and FastAPI.

## Features

- Shorten long URLs to 6-character codes
- Click tracking with live stats polling (every 5 seconds)
- Lookup existing short URLs to view click stats
- Copy to clipboard support
- Dark-themed, responsive single-page frontend
- RESTful API with interactive docs

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

The app will be available at `http://localhost:8000`.

### Run tests

```bash
pytest -v
```

### Lint

```bash
ruff check .
```

## API Endpoints

Interactive docs available at `http://localhost:8000/docs` when the server is running.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Web UI |
| `GET` | `/health` | Health check |
| `GET` | `/info` | Project info (name, version, description) |
| `POST` | `/shorten` | Shorten a URL |
| `GET` | `/stats/{code}` | Get click stats for a short link |
| `GET` | `/{code}` | Redirect to original URL (307) |

### Examples

```bash
# Shorten a URL
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/path"}'

# Get stats
curl http://localhost:8000/stats/aB3xYz

# Redirect
curl -L http://localhost:8000/aB3xYz
```

## Docker

```bash
# Build and run with compose
docker compose up --build

# Or build and run manually
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
