from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.articles.schemas import PaginatedArticles
from app.articles.service import get_latest_articles_page, should_refresh_articles, run_ingestion

router = APIRouter()


@router.get("/articles", response_model=PaginatedArticles)
def get_articles(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    # Lazy-refresh: check if we need to fetch new articles
    if should_refresh_articles(db):
        try:
            run_ingestion()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Ingestion error during lazy refresh: {e}")

    items, pagination = get_latest_articles_page(
        db, limit=limit, cursor=cursor, category=category
    )
    return {"data": items, "pagination": pagination}
