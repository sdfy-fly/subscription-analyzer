from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str | None


class CreateUserResponse(BaseModel):
    token: str


class AuthUserRequest(BaseModel):
    username: str
    password: str


class AuthUserResponse(BaseModel):
    token: str


class GetUserResponse(BaseModel):
    id: UUID
    username: str
    created_at: datetime
