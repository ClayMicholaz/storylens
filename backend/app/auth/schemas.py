from uuid import UUID

from pydantic import BaseModel, Field


class AuthCredentials(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=128)


class AuthUser(BaseModel):
    id: UUID
    email: str


class AuthResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    user: AuthUser

class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1)