from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entity.user import User


@dataclass
class BaseUserRepository(ABC):
    @abstractmethod
    async def is_username_exists(self, username: str) -> bool: ...

    @abstractmethod
    async def is_email_exists(self, email: str) -> bool: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    # TODO: добавить auth
