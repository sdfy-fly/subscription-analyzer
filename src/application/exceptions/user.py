from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.base import ApplicationException


@dataclass
class UsernameAlreadyExists(ApplicationException):
    @property
    def message(self):
        return 'Username уже занят!'


@dataclass
class EmailAlreadyExists(ApplicationException):
    @property
    def message(self):
        return 'Почта уже занята!'


@dataclass
class UserNotFound(ApplicationException):
    user_id: UUID

    @property
    def message(self):
        return f'Пользователя с id="{self.user_id}" не найден!'
