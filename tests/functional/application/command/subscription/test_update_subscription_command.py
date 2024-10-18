from uuid import uuid4

import pytest

from src.application.commands.subscription.update_subscription_command import UpdateSubscriptionCommand
from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.subscription import SubscriptionAlreadyExists
from src.domain.entity.subscription import Subscription
from src.domain.helpers import get_utc_now


async def test_update_subscription_command__ok(mediator, insert_user, insert_category, insert_subscription):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    subscription_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id, name='category 1')
    await insert_subscription(subscription_id=subscription_id, category_id=None, user_id=user_id)
    command = UpdateSubscriptionCommand(
        subscription_id=subscription_id,
        name='updated subscription',
        cost=123,
        budget=123,
        start_date=get_utc_now(),
        expired_date=get_utc_now(),
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        category_id=category_id,
    )

    # act
    subscription: Subscription = await mediator.handle_command(command)

    # assert
    assert subscription is not None
    assert subscription.id == subscription_id
    assert subscription.name.value == 'updated subscription'
    assert subscription.cost.value == 123
    assert subscription.budget.value == 123
    assert subscription.user_id == user_id
    assert subscription.category.id == category_id


async def test_update_subscription_command__remove_category(
    mediator, insert_user, insert_category, insert_subscription
):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    subscription_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id, name='category 1')
    await insert_subscription(subscription_id=subscription_id, category_id=category_id, user_id=user_id)
    command = UpdateSubscriptionCommand(
        subscription_id=subscription_id,
        name='updated subscription',
        cost=123,
        budget=123,
        start_date=get_utc_now(),
        expired_date=get_utc_now(),
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        category_id=None,
    )

    # act
    subscription: Subscription = await mediator.handle_command(command)

    # assert
    assert subscription is not None
    assert subscription.id == subscription_id
    assert subscription.name.value == 'updated subscription'
    assert subscription.user_id == user_id
    assert subscription.category is None


async def test_update_subscription_command__category_does_not_exists(
    mediator, insert_user, insert_category, insert_subscription
):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    subscription_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id, user_id=user_id)
    command = UpdateSubscriptionCommand(
        subscription_id=subscription_id,
        name='updated subscription',
        cost=123,
        budget=123,
        start_date=get_utc_now(),
        expired_date=get_utc_now(),
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        category_id=category_id,
    )

    # act
    with pytest.raises(CategoryNotFound):
        await mediator.handle_command(command)


async def test_update_subscription_command__subscription_already_exists(
    mediator, insert_user, insert_category, insert_subscription
):
    # arrange
    user_id = uuid4()
    subscription_id_1 = uuid4()
    subscription_id_2 = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id_1, user_id=user_id, name='subscription 1')
    await insert_subscription(subscription_id=subscription_id_2, user_id=user_id, name='subscription 2')
    command = UpdateSubscriptionCommand(
        subscription_id=subscription_id_1,
        name='subscription 2',
        cost=123,
        budget=123,
        start_date=get_utc_now(),
        expired_date=get_utc_now(),
        notification_on_expire=True,
        notification_on_budget_threshold=False,
        user_id=user_id,
        category_id=None,
    )

    # act
    with pytest.raises(SubscriptionAlreadyExists):
        await mediator.handle_command(command)
