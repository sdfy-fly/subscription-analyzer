from dataclasses import dataclass

from src.services.exceptions.base import ServiceException


@dataclass
class UsernameAlreadyExists(ServiceException):
    @property
    def message(self):
        return 'Username уже занят!'


@dataclass
class EmailAlreadyExists(ServiceException):
    @property
    def message(self):
        return 'Почта уже занята!'
