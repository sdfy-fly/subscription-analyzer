from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager


class BaseSessionFactory(ABC):
    @abstractmethod
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator: ...
