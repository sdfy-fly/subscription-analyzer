from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class BaseQuery: ...


QR = TypeVar('QR', bound=Any)


class BaseQueryHandler(ABC, Generic[QR]):
    @abstractmethod
    async def handle(self, query: BaseQuery) -> QR: ...
