@router.get("/preferences")
def get_preferences(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    prefs = db.query(UserPreferences).filter(
        UserPreferences.user_id == current_user["id"]
    ).first()
    return prefs