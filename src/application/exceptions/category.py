from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.base import ApplicationException


@dataclass
class CategoryAlreadyExists(ApplicationException):
    @property
    def message(self):
        return 'Такая категория уже существует!'


@dataclass
class CategoryNotFound(ApplicationException):
    category_id: UUID

    @property
    def message(self):
        return f'Категория с id="{self.category_id}" не найдена!'
