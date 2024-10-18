from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.domain.entity.category import Category
from src.domain.entity.subscription import Subscription
from src.domain.exceptions.subscription import (
    SubscriptionBudgetMustBePositive,
    SubscriptionCostMustBePositive,
    SubscriptionInvalidDate,
    SubscriptionNameRequired,
    SubscriptionNameTooLong,
)
from src.domain.helpers import get_utc_now
from src.domain.values.category import Name as CategoryName
from src.domain.values.subscription import Budget, Cost, Name


def get_subscription(
    name: str = 'name',
    cost: float = 123,
    budget: float = 123,
    start_date: datetime | None = None,
    expired_date: datetime | None = None,
):
    start_date = start_date if start_date else get_utc_now()
    expired_date = expired_date if expired_date else get_utc_now()

    return Subscription(
        name=Name(value=name),
        category=None,
        cost=Cost(value=cost),
        budget=Budget(value=budget),
        start_date=start_date,
        expired_date=expired_date,
        user_id=uuid4(),
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
    assert str(e.value.message) == message


@pytest.mark.parametrize(
    'cost, message',
    [
        (0, 'Цена подписки должна быть положительной!'),
        (-123, 'Цена подписки должна быть положительной!'),
    ],
)
def test_subscription__invalid_cost(cost, message):
    # act
    with pytest.raises(SubscriptionCostMustBePositive) as e:
        get_subscription(cost=cost)

    # assert
    assert str(e.value.message) == message


@pytest.mark.parametrize(
    'budget, message',
    [
        (0, 'Бюджет подписки должен быть положительным!'),
        (-123, 'Бюджет подписки должен быть положительным!'),
    ],
)
def test_subscription__invalid_budget(budget, message):
    # act
    with pytest.raises(SubscriptionBudgetMustBePositive) as e:
        get_subscription(budget=budget)

    # assert
    assert str(e.value.message) == message


@pytest.mark.parametrize(
    'start_date, expired_date, message',
    [
        (
            datetime(day=1, month=1, year=2020, tzinfo=UTC),
            datetime(day=1, month=1, year=2010, tzinfo=UTC),
            'Дата начала подписки не может быть позже даты истечения',
        ),
    ],
)
def test_subscription__invalid_date(start_date, expired_date, message):
    # act
    with pytest.raises(SubscriptionInvalidDate) as e:
        get_subscription(start_date=start_date, expired_date=expired_date)

    # assert
    assert str(e.value.message) == message


def test_subscription__ok():
    # arrange
    name = Name(value='some name')
    user_id = uuid4()
    cost = Cost(123)
    budget = Budget(123)
    now = get_utc_now()
    category = Category(name=CategoryName('category 1'), user_id=user_id)

    # act
    subscription = Subscription(
        name=name, cost=cost, start_date=now, expired_date=now, user_id=user_id, budget=budget, category=category
    )

    # assert
    assert subscription.name.value == 'some name'
    assert subscription.cost.value == 123
    assert subscription.budget.value == 123
    assert subscription.category == category
    assert subscription.start_date == now
    assert subscription.expired_date == now
    assert subscription.user_id == user_id
