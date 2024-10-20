from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateUserRequestSchema(BaseModel):
    username: str
    password: str
    email: str | None


class CreateUserResponseSchema(BaseModel):
    token: str


class GetUserResponseSchema(BaseModel):
    id: UUID
    username: str
    created_at: datetime
