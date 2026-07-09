from datetime import datetime
import uuid

from sqlalchemy import Text, DateTime, String, Index
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.database.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)

    source: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    published_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    category: Mapped[str] = mapped_column(Text, nullable=False)

    article_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (
        Index("ix_articles_published_id", "published_date", "id"),
    )