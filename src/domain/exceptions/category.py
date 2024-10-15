from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass
class CategoryNameRequired(ApplicationException):
    def message(self):
        return 'Категории необходимо задать название!'


@dataclass
class CategoryNameTooLong(ApplicationException):
    name: str

    def message(self):
        return f'Слишком длинное название для категории: {self.name}'
