from dataclasses import dataclass

from src.domain.exceptions.subscription import SubscriptionNameRequired, SubscriptionNameTooLong, \
    SubscriptionCostMustBePositive
from src.domain.values.base import BaseValueObject


@dataclass
class SubscriptionId:
    ...


@dataclass(frozen=True)
class Name(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value:
            raise SubscriptionNameRequired

        if len(self.value) > 255:
            raise SubscriptionNameTooLong(self.value)


@dataclass(frozen=True)
class Cost(BaseValueObject[float]):
    value: float

    def validate(self):
        if self.value <= 0:
            raise SubscriptionCostMustBePositive
