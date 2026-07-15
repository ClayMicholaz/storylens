from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.orm import Session

from app.articles.models import Article
from app.articles.repository import get_articles_page
from tests.conftest import make_article


def _insert_articles(db: Session, articles: list[dict]) -> list[Article]:
    """Insert article dicts into the database and return ORM objects."""
    orm_articles = [Article(**a) for a in articles]
    for a in orm_articles:
        db.add(a)
    db.commit()
    for a in orm_articles:
        db.refresh(a)
    return orm_articles


class TestRepository:
    def test_articles_ordered_desc_by_date(self, db_session: Session):
        """Articles are returned newest-first."""
        now = datetime.now(timezone.utc)
        articles = _insert_articles(
            db_session,
            [
                make_article(title="Oldest", published_date=now - timedelta(hours=2)),
                make_article(title="Middle", published_date=now - timedelta(hours=1)),
                make_article(title="Newest", published_date=now),
            ],
        )

        result = get_articles_page(db_session, limit=10)
        titles = [a.title for a in result]
        assert titles == ["Newest", "Middle", "Oldest"], f"Expected newest-first, got {titles}"

    def test_cursor_pagination(self, db_session: Session):
        """Cursor pagination returns articles after (older than) the cursor."""
        now = datetime.now(timezone.utc)
        articles = _insert_articles(
            db_session,
            [
                make_article(title="Article 1", published_date=now - timedelta(hours=3)),
                make_article(title="Article 2", published_date=now - timedelta(hours=2)),
                make_article(title="Article 3", published_date=now - timedelta(hours=1)),
                make_article(title="Article 4", published_date=now),
            ],
        )

        # Repository returns limit+1 to check for has_more (service slices it)
        # With limit=2, it returns 3 (2 requested + 1 overflow check)
        page1 = get_articles_page(db_session, limit=2)
        assert len(page1) == 3
        assert page1[0].title == "Article 4"

        # Use the second article as cursor for a proper pagination test
        cursor_article = page1[1]  # Article 3
        page2 = get_articles_page(
            db_session,
            limit=2,
            cursor_pd=cursor_article.published_date,
            cursor_id=cursor_article.id,
        )
        assert len(page2) == 2  # Articles 2 and 1
        assert page2[0].title == "Article 2"
        assert page2[1].title == "Article 1"

    def test_category_filter(self, db_session: Session):
        """Category filter only returns articles in that category."""
        _insert_articles(
            db_session,
            [
                make_article(title="Tech Article", category="tech"),
                make_article(title="Science Article", category="science"),
                make_article(title="Another Tech", category="tech"),
            ],
        )

        tech_results = get_articles_page(db_session, limit=10, category="tech")
        assert len(tech_results) == 2
        assert all(a.category == "tech" for a in tech_results)

        science_results = get_articles_page(db_session, limit=10, category="science")
        assert len(science_results) == 1
        assert science_results[0].category == "science"

    def test_empty_database(self, db_session: Session):
        """Querying an empty database returns an empty list."""
        result = get_articles_page(db_session, limit=10)
        assert result == []