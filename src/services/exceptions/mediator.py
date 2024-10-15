from dataclasses import dataclass

from src.services.commands.base import BaseCommand
from src.services.exceptions.base import ServiceException


@dataclass
class CommandHandlerNotFound(ServiceException):
    command: type[BaseCommand]

    @property
    def message(self):
        return f'Не найден обработчик для команды: {self.command}'
