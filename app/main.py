import os

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.crud import create_short_link, get_link_by_code, increment_click_count
from app.database import Base, engine, get_db
from app.schemas import HealthResponse, StatsResponse, URLRequest, URLResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SwiftLink",
    description="A fast and simple URL shortener API",
    version="1.0.0",
)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "ok"}


@app.get("/info")
def get_info():
    return {
        "project": "SwiftLink",
        "version": "1.0.0",
        "description": "SwiftLink URL Shortener API",
    }


@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    link = create_short_link(db, str(request.url))
    return URLResponse(
        short_code=link.short_code,
        short_url=f"{BASE_URL}/{link.short_code}",
        original_url=link.original_url,
    )


@app.get("/stats/{code}", response_model=StatsResponse)
def get_stats(code: str, db: Session = Depends(get_db)):
    link = get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    return StatsResponse(
        short_code=link.short_code,
        original_url=link.original_url,
        click_count=link.click_count,
        created_at=link.created_at,
    )


@app.get("/", include_in_schema=False)
def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/{code}")
def redirect_to_url(code: str, db: Session = Depends(get_db)):
    link = get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Short link not found")
    increment_click_count(db, link)
    return RedirectResponse(url=link.original_url, status_code=307)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
