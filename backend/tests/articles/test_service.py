from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from sqlalchemy.orm import Session

from app.articles.service import (
    encode_cursor,
    decode_cursor,
    get_latest_articles_page,
)
from app.articles.models import Article
from tests.conftest import make_article


def _insert_articles(db: Session, count: int) -> list[Article]:
    """Insert `count` articles spaced 1 hour apart and return them."""
    now = datetime.now(timezone.utc)
    articles = []
    for i in range(count):
        a_dict = make_article(
            title=f"Article {i}",
            published_date=now - timedelta(hours=i),
        )
        a = Article(**a_dict)
        db.add(a)
        articles.append(a)
    db.commit()
    for a in articles:
        db.refresh(a)
    return articles


class TestCursorEncoding:
    def test_encode_decode_round_trip(self):
        """Encoding then decoding a cursor returns the original values."""
        pd = datetime(2025, 6, 15, 10, 30, 0, tzinfo=timezone.utc)
        aid = uuid4()

        cursor = encode_cursor(pd, aid)
        decoded_pd, decoded_id = decode_cursor(cursor)

        assert decoded_pd == pd
        assert decoded_id == aid

    def test_cursor_base64_url_safe(self):
        """Encoded cursor is a URL-safe base64 string."""
        cursor = encode_cursor(datetime.now(timezone.utc), uuid4())
        # Should be a string containing only URL-safe characters
        assert isinstance(cursor, str)
        assert "+" not in cursor  # base64 URL-safe uses - instead of +
        assert "/" not in cursor  # base64 URL-safe uses _ instead of /


class TestGetLatestArticlesPage:
    def test_has_more_when_more_exist(self, db_session: Session):
        """Returns has_more=True when there are more articles than the page limit."""
        _insert_articles(db_session, 5)  # More than 3

        items, pagination = get_latest_articles_page(db_session, limit=3)
        assert len(items) == 3
        assert pagination["has_more"] is True
        assert pagination["next_cursor"] is not None

    def test_no_more_when_at_end(self, db_session: Session):
        """Returns has_more=False when all articles fit in one page."""
        _insert_articles(db_session, 3)  # Exactly 3

        items, pagination = get_latest_articles_page(db_session, limit=3)
        assert len(items) == 3
        assert pagination["has_more"] is False
        assert pagination["next_cursor"] is None

    def test_cursor_links_pages(self, db_session: Session):
        """Using the next_cursor from page 1 returns the next page of articles."""
        _insert_articles(db_session, 5)

        # Page 1
        page1, pagination = get_latest_articles_page(db_session, limit=2)
        assert len(page1) == 2
        assert pagination["has_more"] is True
        assert pagination["next_cursor"] is not None

        # Page 2 using cursor from page 1
        page2, pagination2 = get_latest_articles_page(
            db_session, limit=2, cursor=pagination["next_cursor"]
        )
        assert len(page2) == 2
        assert pagination2["has_more"] is True  # One more after this

        # Page 3
        page3, pagination3 = get_latest_articles_page(
            db_session, limit=2, cursor=pagination2["next_cursor"]
        )
        assert len(page3) == 1  # Only 1 left
        assert pagination3["has_more"] is False
        assert pagination3["next_cursor"] is None

    def test_empty_database(self, db_session: Session):
        """No articles in the database returns empty data and no next page."""
        items, pagination = get_latest_articles_page(db_session, limit=20)
        assert items == []
        assert pagination["has_more"] is False
        assert pagination["next_cursor"] is None