from dataclasses import dataclass

from src.domain.exceptions.base import DomainException


@dataclass
class SubscriptionNameRequired(DomainException):
    @property
    def message(self):
        return 'Подписке необходимо задать название!'


@dataclass
class SubscriptionNameTooLong(DomainException):
    name: str

    @property
    def message(self):
        return f'Слишком длинное название для подписки: {self.name}'


@dataclass
class SubscriptionCostMustBePositive(DomainException):
    @property
    def message(self):
        return 'Цена подписки должна быть положительной!'


@dataclass
class SubscriptionBudgetMustBePositive(DomainException):
    @property
    def message(self):
        return 'Бюджет подписки должен быть положительным!'


@dataclass
class SubscriptionInvalidDate(DomainException):
    @property
    def message(self):
        return 'Дата начала подписки не может быть позже даты истечения'
