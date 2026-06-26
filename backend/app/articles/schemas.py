from datetime import datetime
from uuid import UUID

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