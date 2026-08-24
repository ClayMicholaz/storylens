from uuid import UUID

from sqlalchemy.orm import Session

from app.users.models import UserPreferences


def get_user_preferences(
    db: Session,
    user_id: UUID,
) -> UserPreferences | None:
    return (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == user_id)
        .first()
    )


def create_user_preferences(
    db: Session,
    user_id: UUID,
    favorite_topics: list[str] | None = None,
    blocked_topics: list[str] | None = None,
    preferred_sources: list[str] | None = None,
) -> UserPreferences:
    preferences = UserPreferences(
        user_id=user_id,
        favorite_topics=favorite_topics or [],
        blocked_topics=blocked_topics or [],
        preferred_sources=preferred_sources or [],
    )

    db.add(preferences)
    db.commit()
    db.refresh(preferences)

    return preferences


def update_user_preferences(
    db: Session,
    preferences: UserPreferences,
    favorite_topics: list[str],
    blocked_topics: list[str],
    preferred_sources: list[str],
) -> UserPreferences:
    preferences.favorite_topics = favorite_topics
    preferences.blocked_topics = blocked_topics
    preferences.preferred_sources = preferred_sources

    db.commit()
    db.refresh(preferences)

    return preferences