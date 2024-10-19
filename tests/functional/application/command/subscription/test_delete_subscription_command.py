from uuid import uuid4

import pytest

from src.application.commands.subscription.delete_subscription_command import DeleteSubscriptionCommand
from src.application.exceptions.common import ForbiddenActionException
from src.application.exceptions.subscription import SubscriptionNotFound


async def test_delete_subscription_command__ok(mediator, insert_user, insert_subscription, pg):
    # arrange
    user_id = uuid4()
    subscription_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id, user_id=user_id)
    command = DeleteSubscriptionCommand(subscription_id=subscription_id, user_id=user_id)

    # act
    await mediator.handle_command(command)

    # assert
    assert not await pg.fetch('SELECT * FROM subscriptions')


async def test_delete_subscription_command__subscription_does_not_exists(mediator):
    # arrange
    subscription_id = uuid4()
    command = DeleteSubscriptionCommand(subscription_id=subscription_id, user_id=uuid4())

    # act
    with pytest.raises(SubscriptionNotFound):
        await mediator.handle_command(command)


async def test_delete_subscription_command__access_denied(mediator, insert_subscription, insert_user):
    # arrange
    subscription_id = uuid4()
    user_id = uuid4()
    random_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id, user_id=user_id)
    command = DeleteSubscriptionCommand(subscription_id=subscription_id, user_id=random_id)

    # act
    with pytest.raises(ForbiddenActionException):
        await mediator.handle_command(command)
