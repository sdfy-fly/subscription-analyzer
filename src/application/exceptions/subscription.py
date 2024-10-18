from dataclasses import dataclass

from src.application.exceptions.base import ApplicationException


@dataclass
class SubscriptionAlreadyExists(ApplicationException):
    @property
    def message(self):
        return 'Такая подписка уже существует!'
