from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass
class ServiceException(ApplicationException):
    @property
    def message(self):
        return 'Сервисная ошибка'
