import threading
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.articles.schemas import PaginatedArticles
from app.articles.service import get_latest_articles_page, should_refresh_articles
from app.ingestion.pipeline import run_ingestion

router = APIRouter()

# Thread-safe flag to prevent concurrent background ingestion runs
_ingestion_lock = threading.Lock()
_ingestion_in_progress = False


@router.get("/articles", response_model=PaginatedArticles)
def get_articles(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None,
):
    """Get articles with async lazy-refresh using BackgroundTasks.
    
    If articles are stale, triggers background ingestion to refresh them
    without blocking the API response.
    """
    # Lazy-refresh: check if we need to fetch new articles
    needs_refresh = should_refresh_articles(db)
    
    if needs_refresh:
        # Thread-safe check and set for background ingestion
        with _ingestion_lock:
            if not _ingestion_in_progress:
                _ingestion_in_progress = True
                background_tasks.add_task(_run_background_ingestion)
    
    items, pagination = get_latest_articles_page(
        db, limit=limit, cursor=cursor, category=category
    )
    return {"data": items, "pagination": pagination}


def _run_background_ingestion():
    """Wrapper for ingestion to track its state and handle errors."""
    global _ingestion_in_progress
    try:
        run_ingestion()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Background ingestion error: {e}")
    finally:
        with _ingestion_lock:
            _ingestion_in_progress = False