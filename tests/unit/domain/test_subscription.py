import pytest

from src.domain.entity.subscription import Subscription
from src.domain.exceptions.subscription import (
    SubscriptionCostMustBePositive,
    SubscriptionNameRequired,
    SubscriptionNameTooLong,
)
from src.domain.helpers import get_utc_now
from src.domain.values.subscription import Cost, Name


def get_subscription(name: str = 'name', cost: float = 123):
    return Subscription(
        name=Name(value=name),
        category=None,
        cost=Cost(value=cost),
        start_date=get_utc_now(),
        expired_date=get_utc_now(),
    )


@pytest.mark.parametrize('name', ['', ' '])
def test_subscription__empty_name(name):
    with pytest.raises(SubscriptionNameRequired) as e:
        get_subscription(name=name)
        assert str(e) == 'Подписке необходимо задать название!'


def test_subscription__name_too_long():
    name = 'name' * 100
    with pytest.raises(SubscriptionNameTooLong) as e:
        get_subscription(name=name)
        assert str(e) == f'Слишком длинное название для подписки: {name}'


def test_subscription__non_positive_price():
    with pytest.raises(SubscriptionCostMustBePositive) as e:
        get_subscription(cost=0)
        assert str(e) == 'Цена подписки должна быть положительной!'
