from dataclasses import dataclass

from src.application.commands.base import BaseCommand
from src.application.exceptions.base import ApplicationException
from src.application.queries.base import BaseQuery


@dataclass
class CommandHandlerNotFound(ApplicationException):
    command: type[BaseCommand]

    @property
    def message(self):
        return f'Не найден обработчик для команды: {self.command}'


@dataclass
class QueryHandlerNotFound(ApplicationException):
    query: type[BaseQuery]

    @property
    def message(self):
        return f'Не найден обработчик для запроса: {self.query}'
