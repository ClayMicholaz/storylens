import os
import tempfile

# Must be set before any app module imports
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ALGORITHM"] = "HS256"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, Text, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import ColumnDefault
from fastapi.testclient import TestClient

# ── Patch UserPreferences ARRAY columns for SQLite ──────────────
from app.users import models as user_models

for col_name in ("favorite_topics", "blocked_topics", "preferred_sources"):
    col = getattr(user_models.UserPreferences.__table__.c, col_name)
    col.type = Text()
    col.default = None

from app.database.base import Base
from app.main import app
from app.database.session import get_db

# ── File-based temporary SQLite database ────────────────────────

_db_fd, _db_path = tempfile.mkstemp(suffix=".sqlite")
TEST_DATABASE_URL = f"sqlite:///{_db_path}"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Must define TestSessionLocal BEFORE using it in the event listener decorator
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

import json


@event.listens_for(TestSessionLocal, "before_flush")
def _serialize_lists(session, flush_context, instances):
    """Convert Python list values to JSON strings before flushing to SQLite."""
    for obj in session.dirty | session.new:
        if hasattr(obj, "favorite_topics") and isinstance(obj.favorite_topics, list):
            obj.favorite_topics = json.dumps(obj.favorite_topics)
        if hasattr(obj, "blocked_topics") and isinstance(obj.blocked_topics, list):
            obj.blocked_topics = json.dumps(obj.blocked_topics)
        if hasattr(obj, "preferred_sources") and isinstance(obj.preferred_sources, list):
            obj.preferred_sources = json.dumps(obj.preferred_sources)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a FastAPI TestClient with overridden DB dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Factory helpers ──────────────────────────────────────────────


def make_article(
    title: str = "Test Article",
    summary: str | None = "A test summary.",
    content: str | None = "Full content here.",
    source: str = "Test Source",
    url: str = "https://example.com/test",
    category: str = "tech",
    published_date: datetime | None = None,
    article_hash: str | None = None,
    content_hash: str | None = None,
) -> dict:
    """Return a dict suitable for inserting into the articles table."""
    import hashlib

    pd = published_date or datetime.now(timezone.utc)
    ah = article_hash or hashlib.sha256(f"{url.strip()}::{title.strip()}".encode("utf-8")).hexdigest()
    ch = content_hash or hashlib.sha256((content or "").strip().encode("utf-8")).hexdigest()
    return {
        "id": uuid4(),
        "title": title,
        "summary": summary,
        "content": content,
        "source": source,
        "url": url,
        "category": category,
        "published_date": pd,
        "article_hash": ah,
        "content_hash": ch,
    }


def make_user_dict(
    email: str = "test@example.com",
    hashed_password: str | None = None,
    is_active: bool = True,
    token_version: int = 0,
) -> dict:
    """Return a dict suitable for inserting into the users table."""
    from app.core.auth import hash_password

    return {
        "id": uuid4(),
        "email": email,
        "hashed_password": hashed_password or hash_password("password123"),
        "is_active": is_active,
        "token_version": token_version,
    }