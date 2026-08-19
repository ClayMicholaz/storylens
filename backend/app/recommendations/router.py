from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.recommendations.schemas import RecommendationsResponse
from app.recommendations.service import get_article_recommendations


router = APIRouter()


@router.get(
    "/articles/{article_id}/recommendations",
    response_model=RecommendationsResponse,
)
def get_recommendations(
    article_id: UUID,
    db: Session = Depends(get_db),
):
    """Get semantically similar articles for an article."""

    article, recommendations = get_article_recommendations(
        db,
        article_id=article_id,
        limit=5,
    )

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return {
        "data": [
            {
                "id": recommendation.id,
                "title": recommendation.title,
                "summary": recommendation.summary,
                "source": recommendation.source,
                "url": recommendation.url,
                "category": recommendation.category,
                "published_date": recommendation.published_date,
                "similarity": float(similarity),
            }
            for recommendation, similarity in recommendations
        ]
    }