from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.recommendations.schemas import RecommendationsResponse
from app.recommendations.service import (
    get_article_recommendations,
    get_personalized_article_recommendations,
)


router = APIRouter(
    tags=["Recommendations"],
)


@router.get(
    "/articles/{article_id}/recommendations",
    response_model=RecommendationsResponse,
)
def get_article_recommendations_route(
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


@router.get(
    "/recommendations",
    response_model=RecommendationsResponse,
)
def get_personalized_recommendations_route(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get personalized article recommendations for the current user."""

    recommendations = get_personalized_article_recommendations(
        db,
        user_id=current_user["id"],
        limit=limit,
    )

    return {
        "data": [
            {
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "source": article.source,
                "url": article.url,
                "category": article.category,
                "published_date": article.published_date,
                "similarity": float(similarity),
            }
            for article, similarity in recommendations
        ]
    }