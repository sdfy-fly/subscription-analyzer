from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.base import ApplicationException


@dataclass
class SubscriptionAlreadyExists(ApplicationException):
    @property
    def message(self):
        return 'Такая подписка уже существует!'


@dataclass
class SubscriptionNotFound(ApplicationException):
    subscription_id: UUID

    @property
    def message(self):
        return f'Подписка с id="{self.subscription_id}" не найдена!'
