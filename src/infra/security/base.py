from abc import ABC, abstractmethod


class BasePasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> bytes: ...

    @abstractmethod
    def verify_password(self, password: str, hashed_password: bytes) -> bool: ...
