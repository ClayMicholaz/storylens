from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserPreferences
from app.schemas.auth import UserCreate, UserLogin, UserOut, TokenResponse
from app.core import auth

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE_NAME = "refresh_token"


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password=auth.hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(UserPreferences(user_id=user.id))
    db.commit()

    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(user.id)
    refresh_token = auth.create_refresh_token(user.id, user.token_version)

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=14 * 24 * 60 * 60,
        path="/auth",
    )
    return {"access_token": access_token}


@router.post("/refresh", response_model=TokenResponse)
def refresh(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = auth.decode_token(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user = db.query(User).filter_by(id=int(payload["sub"])).first()
    if not user or user.token_version != payload.get("ver"):
        raise HTTPException(status_code=401, detail="Token revoked")

    return {"access_token": auth.create_access_token(user.id)}


@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    if token:
        try:
            payload = auth.decode_token(token)
            user = db.query(User).filter_by(id=int(payload["sub"])).first()
            if user:
                user.token_version += 1
                db.commit()
        except ValueError:
            pass

    response.delete_cookie(REFRESH_COOKIE_NAME, path="/auth")
    return {"detail": "Logged out"}