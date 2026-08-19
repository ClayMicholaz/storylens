from uuid import UUID

from sqlalchemy.orm import Session

from app.recommendations.repository import get_similar_articles


def get_article_recommendations(
    db: Session,
    article_id: UUID,
    limit: int = 5,
):
    """Get semantic recommendations for an article."""

    article, recommendations = get_similar_articles(
        db,
        article_id=article_id,
        limit=limit,
    )

    return article, recommendations