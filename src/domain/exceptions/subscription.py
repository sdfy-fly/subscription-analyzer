from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(frozen=True)
class SubscriptionNameRequired(ApplicationException):
    def message(self):
        return 'Подписке необходимо задать название!'


@dataclass(frozen=True)
class SubscriptionNameTooLong(ApplicationException):
    name: str

    def message(self):
        return f'Слишком длинное название для подписки: {self.name}'


@dataclass(frozen=True)
class SubscriptionCostMustBePositive(ApplicationException):
    def message(self):
        return 'Цена подписки должна быть положительной!'


@dataclass(frozen=True)
class SubscriptionBudgetMustBePositive(ApplicationException):
    def message(self):
        return 'Бюджет подписки должен быть положительным!'
