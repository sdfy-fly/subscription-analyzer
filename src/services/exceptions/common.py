from dataclasses import dataclass

from src.services.exceptions.base import ServiceException


@dataclass
class ForbiddenActionException(ServiceException):
    detail: str

    @property
    def message(self):
        return f'Доступ запрещен: {self.detail}'
