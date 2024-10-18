from uuid import uuid4

import pytest

from src.application.commands.subscription.create_subscription_command import CreateSubscriptionCommand
from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.subscription import SubscriptionAlreadyExists
from src.domain.entity.category import Category
from src.domain.entity.subscription import Subscription
from src.domain.helpers import get_utc_now
from src.domain.values.category import Name


async def test_create_subscription_command__ok(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    category = Category(name=Name('category 1'), user_id=user_id)
    command = CreateSubscriptionCommand(
        name='subscription 1',
        cost=123,
        budget=123,
        category_id=category.id,
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        expired_date=get_utc_now(),
        start_date=get_utc_now(),
    )
    await insert_user(user_id=user_id)
    await insert_category(category_id=category.id, user_id=user_id)

    # act
    subscription: Subscription = await mediator.handle_command(command)

    # assert
    assert subscription.name.value == 'subscription 1'
    assert subscription.cost.value == 123
    assert subscription.budget.value == 123
    assert subscription.category.id == category.id
    assert subscription.user_id == user_id


async def test_create_subscription_command__category_does_not_exists(mediator):
    # arrange
    command = CreateSubscriptionCommand(
        name='subscription 1',
        cost=123,
        budget=None,
        category_id=uuid4(),
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=uuid4(),
        expired_date=get_utc_now(),
        start_date=get_utc_now(),
    )

    # act
    with pytest.raises(CategoryNotFound):
        await mediator.handle_command(command)


async def test_create_subscription_command__no_category(mediator, insert_user):
    # arrange
    user_id = uuid4()
    command = CreateSubscriptionCommand(
        name='subscription 1',
        cost=123,
        budget=None,
        category_id=None,
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        expired_date=get_utc_now(),
        start_date=get_utc_now(),
    )
    await insert_user(user_id=user_id)

    # act
    subscription: Subscription = await mediator.handle_command(command)

    # assert
    assert subscription.name.value == 'subscription 1'
    assert subscription.budget is None
    assert subscription.category is None
    assert subscription.user_id == user_id


async def test_create_subscription_command__already_exists(mediator, insert_user, insert_subscription):
    # arrange
    user_id = uuid4()
    command = CreateSubscriptionCommand(
        name='subscription 1',
        cost=123,
        budget=None,
        category_id=None,
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        expired_date=get_utc_now(),
        start_date=get_utc_now(),
    )
    await insert_user(user_id=user_id)
    await insert_subscription(user_id=user_id, name='subscription 1')

    # act
    with pytest.raises(SubscriptionAlreadyExists):
        await mediator.handle_command(command)
