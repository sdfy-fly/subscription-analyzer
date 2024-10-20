from abc import ABC, abstractmethod
from uuid import UUID


class BasePasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> bytes: ...

    @abstractmethod
    def verify_password(self, password: str, hashed_password: bytes) -> bool: ...


class BaseTokenManager(ABC):
    @abstractmethod
    def create_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> UUID: ...
