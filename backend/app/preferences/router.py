from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.deps import get_current_user
from backend.app.database.session import get_db
from backend.app.users.models import UserPreferences

router = APIRouter(prefix="/preferences", tags=["preferences"])


@router.get("/")
def get_preferences(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    prefs = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user["id"]
    ).first()
    return prefs