from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str | None] = mapped_column(Text)

    source: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[str] = mapped_column(Text, nullable=False)

    published_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    article_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)