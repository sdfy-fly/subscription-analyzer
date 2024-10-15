from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


@dataclass(frozen=True)
class BaseCommand: ...


CR = TypeVar('CR', bound=Any)


class BaseCommandHandler(ABC, Generic[CR]):
    @abstractmethod
    async def handle(self, command: BaseCommand) -> CR: ...
