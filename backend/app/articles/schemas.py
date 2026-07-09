from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ArticleResponse(BaseModel):
    id: UUID
    title: str
    summary: str | None
    source: str
    url: str
    category: str
    published_date: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    next_cursor: Optional[str] = None
    has_more: bool
    limit: int


class PaginatedArticles(BaseModel):
    data: list[ArticleResponse]
    pagination: PaginationMeta