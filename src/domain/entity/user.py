from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.domain.entity.base import BaseEntity
from src.domain.values.user import Email, Password, Username


@dataclass(kw_only=True)
class User(BaseEntity):
    id: UUID = field(default_factory=uuid4)
    """Id пользователя"""
    username: Username
    """Username"""
    password: Password
    """Пароль"""
    email: Email | None = None
    """Почта"""
