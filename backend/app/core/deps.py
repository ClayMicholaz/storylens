from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.auth import decode_token
from app.database.session import get_db
from app.users.models import User

security = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    try:
        payload = decode_token(creds.credentials)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    token_version = payload.get("ver")
    if token_version is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = UUID(str(payload.get("sub")))
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")
    if user.token_version != int(token_version):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    token_email = payload.get("email")
    if token_email and token_email != user.email:
        raise HTTPException(status_code=401, detail="Token subject mismatch")

    return {"id": user.id, "email": user.email, "role": payload.get("role"), "token_version": user.token_version}