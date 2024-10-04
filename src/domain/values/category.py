from dataclasses import dataclass

from src.domain.exceptions.category import CategoryNameRequired, CategoryNameTooLong
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Name(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise CategoryNameRequired

        if len(self.value) > 100:
            raise CategoryNameTooLong(self.value)
