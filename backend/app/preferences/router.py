from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.preferences.schemas import (
    PreferencesResponse,
    PreferencesUpdate,
)
from app.preferences.service import (
    get_preferences,
    update_preferences,
)


router = APIRouter(
    prefix="/preferences",
    tags=["Preferences"],
)


@router.get(
    "",
    response_model=PreferencesResponse,
)
def read_preferences(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    preferences = get_preferences(
        db,
        user_id=current_user["id"],
    )

    if preferences is None:
        return PreferencesResponse(
            favorite_topics=[],
            blocked_topics=[],
            preferred_sources=[],
        )

    return preferences


@router.put(
    "",
    response_model=PreferencesResponse,
)
def save_preferences(
    data: PreferencesUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_preferences(
        db,
        user_id=current_user["id"],
        data=data,
    )