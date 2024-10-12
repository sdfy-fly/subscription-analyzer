from datetime import datetime
from uuid import UUID, uuid4

import pytest

from src.domain.entity.category import Category
from src.domain.entity.subscription import Subscription
from src.domain.helpers import get_utc_now
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.domain.values.category import Name as CategoryName
from src.domain.values.subscription import Budget, Cost, Name


@pytest.fixture(name='subscription_repo')
async def get_subscription_repo(container, pg_session):
    repo: BaseSubscriptionRepository = container.resolve(BaseSubscriptionRepository, session=pg_session)
    yield repo


def get_subscription(
    name: str,
    cost: float,
    user_id: UUID,
    budget: float | None = None,
    category: Category | None = None,
    now: datetime | None = None,
):
    now = now if now else get_utc_now()
    budget = Budget(budget) if budget else None

    return Subscription(
        name=Name(name),
        cost=Cost(cost),
        budget=budget,
        start_date=now,
        expired_date=now,
        user_id=user_id,
        category=category,
    )


async def test_subscription__create(insert_user, insert_category, subscription_repo, pg_session, pg):
    # arrange
    now = get_utc_now()
    user_id = uuid4()
    category = Category(name=CategoryName('category 1'), user_id=user_id)
    subscription = get_subscription(
        name='subscription 1', cost=123, budget=123, category=category, user_id=user_id, now=now
    )

    await insert_user(user_id=user_id)
    await insert_category(category_id=category.id, name=category.name.value, user_id=user_id)

    # act
    await subscription_repo.create(subscription)
    await pg_session.commit()

    # assert
    subscriptions_from_db = await pg.fetch('SELECT * FROM subscriptions')
    assert len(subscriptions_from_db) == 1
    subscription_from_db = subscriptions_from_db[0]

    assert subscription_from_db['id'] == subscription.id
    assert subscription_from_db['name'] == subscription.name.value
    assert subscription_from_db['cost'] == subscription.cost.value
    assert subscription_from_db['budget'] == subscription.budget.value
    assert subscription_from_db['start_date'] == subscription.start_date
    assert subscription_from_db['expired_date'] == subscription.expired_date
    assert subscription_from_db['user_id'] == subscription.user_id
    assert subscription_from_db['category_id'] == category.id
    assert subscription_from_db['notification_on_expire'] == subscription.notification_on_expire
    assert subscription_from_db['notification_on_budget_threshold'] == subscription.notification_on_budget_threshold
    assert subscription_from_db['created_at'] == subscription.created_at
    assert subscription_from_db['updated_at'] == subscription.updated_at


@pytest.mark.parametrize(
    'old_name, new_name, expected_result',
    [
        ('subscription 1', 'subscription 2', False),
        ('subscription 1', 'subscription 1', True),
    ],
)
async def test_subscription__is_subscription_exists(
    subscription_repo, insert_user, old_name, new_name, expected_result
):
    # arrange
    user_id = uuid4()
    subscription1 = get_subscription(name=old_name, cost=100, user_id=user_id)
    subscription2 = get_subscription(name=new_name, cost=100, user_id=user_id)
    await insert_user(user_id=user_id)
    await subscription_repo.create(subscription1)

    # act
    result = await subscription_repo.is_subscription_exists(subscription2)

    # assert
    assert result is expected_result


async def test_subscription__get_by_id(subscription_repo, insert_user):
    # arrange
    user_id = uuid4()
    subscription = get_subscription(name='subscription 1', cost=100, user_id=user_id)
    await insert_user(user_id=user_id)
    await subscription_repo.create(subscription)

    # act
    subscription_from_db = await subscription_repo.get_by_id(subscription.id)

    # assert
    assert subscription_from_db is not None
    assert subscription_from_db == subscription


async def test_subscription__get_by_id__not_found(subscription_repo):
    # arrange
    subscription_id = uuid4()

    # act
    subscription_from_db = await subscription_repo.get_by_id(subscription_id)

    # assert
    assert subscription_from_db is None


async def test_subscription__get_user_subscription(subscription_repo, insert_user):
    # arrange
    user_id = uuid4()
    subscription1 = get_subscription(name='subscription 1', cost=100, user_id=user_id)
    subscription2 = get_subscription(name='subscription 2', cost=200, user_id=user_id)
    await insert_user(user_id=user_id)
    await subscription_repo.create(subscription1)
    await subscription_repo.create(subscription2)

    # act
    user_subscriptions = await subscription_repo.get_user_subscription(user_id)

    # assert
    assert user_subscriptions == [subscription1, subscription2]


async def test_subscription__get_user_subscription__empty(subscription_repo, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)

    # act
    user_subscriptions = await subscription_repo.get_user_subscription(user_id)

    # assert
    assert user_subscriptions == []


@pytest.mark.asyncio
async def test_subscription__update(insert_user, insert_category, subscription_repo, pg_session, pg):
    # arrange
    user_id = uuid4()
    category = Category(name=CategoryName('category 1'), user_id=user_id)
    subscription = get_subscription(name='subscription 1', cost=123, budget=321, user_id=user_id, category=category)
    await insert_user(user_id=user_id)
    await insert_category(category_id=category.id, user_id=user_id)
    await subscription_repo.create(subscription)

    # act
    subscription.name = Name('updated subscription 1')
    subscription.cost = Cost(321)
    subscription.budget = None
    subscription.category = None
    updated_subscription = await subscription_repo.update(subscription)
    await pg_session.commit()

    # assert
    # проверяем ответ репозитория
    assert updated_subscription is not None
    assert updated_subscription.id == subscription.id
    assert updated_subscription.name.value == 'updated subscription 1'
    assert updated_subscription.cost.value == 321
    assert updated_subscription.budget is None
    assert updated_subscription.user_id == user_id
    assert updated_subscription.category is None
    assert updated_subscription.created_at == subscription.created_at
    assert updated_subscription.updated_at > subscription.updated_at

    # проверяем обновление в базе
    subscriptions_in_db = await pg.fetch('SELECT * FROM subscriptions')
    assert len(subscriptions_in_db) == 1
    subscription_in_db = subscriptions_in_db[0]
    assert subscription_in_db['id'] == subscription.id
    assert subscription_in_db['name'] == 'updated subscription 1'
    assert subscription_in_db['cost'] == 321
    assert subscription_in_db['budget'] is None
    assert subscription_in_db['user_id'] == user_id
    assert subscription_in_db['category_id'] is None
    assert subscription_in_db['created_at'] == subscription.created_at
    assert subscription_in_db['updated_at'] > subscription.updated_at
