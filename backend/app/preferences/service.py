from uuid import UUID

from sqlalchemy.orm import Session

from app.preferences.repository import (
    create_user_preferences,
    get_user_preferences,
    update_user_preferences,
)
from app.preferences.schemas import PreferencesUpdate


def get_preferences(
    db: Session,
    user_id: UUID,
):
    return get_user_preferences(
        db,
        user_id=user_id,
    )


def update_preferences(
    db: Session,
    user_id: UUID,
    data: PreferencesUpdate,
):
    preferences = get_user_preferences(
        db,
        user_id=user_id,
    )

    if preferences is None:
        return create_user_preferences(
            db,
            user_id=user_id,
            favorite_topics=data.favorite_topics,
            blocked_topics=data.blocked_topics,
            preferred_sources=data.preferred_sources,
        )

    return update_user_preferences(
        db,
        preferences=preferences,
        favorite_topics=data.favorite_topics,
        blocked_topics=data.blocked_topics,
        preferred_sources=data.preferred_sources,
    )