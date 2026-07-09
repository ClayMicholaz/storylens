import base64
import json
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.articles.repository import get_articles_page as repo_get_articles_page


def encode_cursor(published_date: datetime, article_id: UUID) -> str:
    payload = {"pd": published_date.isoformat(), "id": str(article_id)}
    raw = json.dumps(payload).encode()
    return base64.urlsafe_b64encode(raw).decode()


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    raw = base64.urlsafe_b64decode(cursor.encode())
    payload = json.loads(raw)
    return datetime.fromisoformat(payload["pd"]), UUID(payload["id"])


def get_latest_articles_page(
    db: Session,
    limit: int = 20,
    cursor: Optional[str] = None,
    category: Optional[str] = None,
):
    cursor_pd, cursor_id = decode_cursor(cursor) if cursor else (None, None)

    items = repo_get_articles_page(
        db, limit=limit, cursor_pd=cursor_pd, cursor_id=cursor_id, category=category
    )

    has_more = len(items) > limit
    items = items[:limit]
    next_cursor = (
        encode_cursor(items[-1].published_date, items[-1].id)
        if has_more and items
        else None
    )

    data = [
        {
            "id": a.id,
            "title": a.title,
            "summary": a.summary,
            "url": a.url,
            "source": a.source,
            "category": a.category,
            "published_date": a.published_date,
        }
        for a in items
    ]

    return data, {
        "next_cursor": next_cursor,
        "has_more": has_more,
        "limit": limit,
    }