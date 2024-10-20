from abc import ABC, abstractmethod
from uuid import UUID


class BasePasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool: ...


class BaseTokenManager(ABC):
    @abstractmethod
    def create_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> UUID: ...
