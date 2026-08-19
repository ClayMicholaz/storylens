from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    id: UUID
    title: str
    summary: str | None
    source: str
    url: str
    category: str
    published_date: datetime
    similarity: float

    model_config = ConfigDict(from_attributes=True)


class RecommendationsResponse(BaseModel):
    data: list[RecommendationResponse]