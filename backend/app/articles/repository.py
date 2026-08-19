from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import desc, tuple_, func

from app.articles.models import Article


def get_latest_article_timestamp(db: Session) -> Optional[datetime]:
    """Get the timestamp of the most recently published article."""
    result = db.query(func.max(Article.published_date)).scalar()
    return result


def get_articles_page(
    db: Session,
    limit: int,
    cursor_pd: Optional[datetime] = None,
    cursor_id: Optional[UUID] = None,
    category: Optional[str] = None,
):
    query = db.query(Article)

    if category:
        query = query.filter(Article.category == category)

    if cursor_pd is not None and cursor_id is not None:
        query = query.filter(
            tuple_(Article.published_date, Article.id)
            < (cursor_pd, cursor_id)
        )

    query = query.order_by(
        desc(Article.published_date),
        desc(Article.id)
    )

    return query.limit(limit + 1).all()


def get_article_by_id(
    db: Session,
    article_id: UUID,
) -> Optional[Article]:
    """Get a single article by ID."""
    return (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )