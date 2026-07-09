from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.articles.schemas import PaginatedArticles
from backend.app.articles.service import get_latest_articles_page

router = APIRouter()


@router.get("/articles", response_model=PaginatedArticles)
def get_articles(
    limit: int = Query(20, ge=1, le=100),
    cursor: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    items, pagination = get_latest_articles_page(
        db, limit=limit, cursor=cursor, category=category
    )
    return {"data": items, "pagination": pagination}