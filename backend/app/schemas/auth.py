from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PreferencesUpdate(BaseModel):
    favorite_topics: List[str] = []
    blocked_topics: List[str] = []
    preferred_sources: List[str] = []