from dataclasses import dataclass

from src.services.exceptions.base import ServiceException


@dataclass
class CategoryAlreadyExists(ServiceException):
    @property
    def message(self):
        return 'Такая категория уже существует!'
