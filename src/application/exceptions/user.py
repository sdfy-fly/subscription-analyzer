from dataclasses import dataclass

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
