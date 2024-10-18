from dataclasses import dataclass

from src.domain.exceptions.base import DomainException


@dataclass
class ApplicationException(DomainException):
    @property
    def message(self):
        return 'Ошибка приложения'
