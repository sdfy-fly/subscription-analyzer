from dataclasses import dataclass

from src.application.exceptions.base import ApplicationException


@dataclass
class ForbiddenActionException(ApplicationException):
    detail: str

    @property
    def message(self):
        return f'Доступ запрещен: {self.detail}'
