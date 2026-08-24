from uuid import UUID

from sqlalchemy.orm import Session

from app.embeddings.service import embedding_service
from app.preferences.repository import get_user_preferences
from app.recommendations.repository import (
    get_personalized_recommendations,
    get_similar_articles,
)


def get_article_recommendations(
    db: Session,
    article_id: UUID,
    limit: int = 5,
):
    """Get semantic recommendations for an article."""

    return get_similar_articles(
        db,
        article_id=article_id,
        limit=limit,
    )


def build_preference_text(
    favorite_topics: list[str],
    blocked_topics: list[str],
    preferred_sources: list[str],
) -> str:
    """Build text representing a user's content preferences."""

    favorite_topics_text = ", ".join(favorite_topics)
    blocked_topics_text = ", ".join(blocked_topics)
    preferred_sources_text = ", ".join(preferred_sources)

    return (
        f"Favorite topics: {favorite_topics_text}. "
        f"Preferred sources: {preferred_sources_text}. "
        f"Topics to avoid: {blocked_topics_text}."
    )


def get_personalized_article_recommendations(
    db: Session,
    user_id: UUID,
    limit: int = 10,
):
    """Get articles personalized to the user's preferences."""

    preferences = get_user_preferences(
        db,
        user_id=user_id,
    )

    if preferences is None:
        return []

    preference_text = build_preference_text(
        favorite_topics=preferences.favorite_topics or [],
        blocked_topics=preferences.blocked_topics or [],
        preferred_sources=preferences.preferred_sources or [],
    )

    user_embedding = embedding_service.generate_text(
        preference_text,
    )

    return get_personalized_recommendations(
        db,
        user_embedding=user_embedding,
        limit=limit,
    )