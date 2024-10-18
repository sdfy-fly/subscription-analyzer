from dataclasses import dataclass

from src.domain.exceptions.base import DomainException


@dataclass
class CategoryNameRequired(DomainException):
    @property
    def message(self):
        return 'Категории необходимо задать название!'


@dataclass
class CategoryNameTooLong(DomainException):
    name: str

    @property
    def message(self):
        return f'Слишком длинное название для категории: {self.name}'
