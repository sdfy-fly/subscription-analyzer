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


@pytest.mark.parametrize(
    'name, exception, message',
    [
        ('', SubscriptionNameRequired, 'Подписке необходимо задать название!'),
        (' ', SubscriptionNameRequired, 'Подписке необходимо задать название!'),
        ('x' * 256, SubscriptionNameTooLong, f'Слишком длинное название для подписки: {"x" * 256}'),
    ],
)
def test_category__invalid_name(name, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_subscription(name=name)

    # assert
    assert str(e.value.message()) == message


@pytest.mark.parametrize(
    'cost, exception, message',
    [
        (0, SubscriptionCostMustBePositive, 'Цена подписки должна быть положительной!'),
        (-123, SubscriptionCostMustBePositive, 'Цена подписки должна быть положительной!'),
    ],
)
def test_subscription__invalid_price(cost, exception, message):
    # act
    with pytest.raises(exception) as e:
        get_subscription(cost=cost)

    # assert
    assert str(e.value.message()) == message


def test_subscription__ok():
    # arrange
    name = Name(value='some name')
    cost = Cost(123)

    # act
    subscription = Subscription(name=name, cost=cost, start_date=get_utc_now(), expired_date=get_utc_now())

    # assert
    assert subscription.name.value == 'some name'
    assert subscription.cost.value == 123
