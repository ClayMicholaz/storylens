from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.schemas import AuthCredentials, AuthResponse, AuthUser, RefreshRequest
from app.core.auth import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    decode_token
)
from app.database.session import get_db
from app.users.models import User, UserPreferences

router = APIRouter(prefix="/auth", tags=["Auth"])


def _build_auth_response(user: User) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(user.id, user.email, user.token_version),
        refresh_token=create_refresh_token(user.id, user.email, user.token_version),
        user=AuthUser(id=user.id, email=user.email),
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: AuthCredentials, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email is already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.flush()
    db.add(UserPreferences(user_id=user.id))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered")

    db.refresh(user)
    return _build_auth_response(user)


@router.post("/login", response_model=AuthResponse)
def login(payload: AuthCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")

    return _build_auth_response(user)

@router.post("/refresh", response_model=AuthResponse)
def refresh_tokens(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        token_data = decode_token(payload.refresh_token)

        if token_data.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = UUID(str(token_data.get("sub")))
        token_version = int(token_data.get("ver"))

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if user.token_version != token_version:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")

    if token_data.get("email") != user.email:
        raise HTTPException(status_code=401, detail="Refresh token subject mismatch")

    return _build_auth_response(user)