from uuid import uuid4

import pytest

from src.application.exceptions.common import ForbiddenActionException
from src.application.exceptions.subscription import SubscriptionNotFound
from src.application.queries.subscription.get_subscription_by_id_query import GetSubscriptionByIdQuery


async def test_get_subscription_by_id_query__ok(mediator, insert_user, insert_subscription):
    # arrange
    subscription_id = uuid4()
    user_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id, user_id=user_id)
    query = GetSubscriptionByIdQuery(subscription_id=subscription_id, user_id=user_id)

    # act
    subscription = await mediator.handle_query(query)

    # assert
    assert subscription.id == subscription_id


async def test_get_subscription_by_id_query__not_found(mediator, insert_user):
    # arrange
    subscription_id = uuid4()
    query = GetSubscriptionByIdQuery(subscription_id=subscription_id, user_id=uuid4())

    # act
    with pytest.raises(SubscriptionNotFound) as e:
        await mediator.handle_query(query)

    # assert
    assert e.value.message == f'Подписка с id="{subscription_id}" не найдена!'


async def test_get_subscription_by_id_query__access_denied(mediator, insert_user, insert_subscription):
    # arrange
    subscription_id = uuid4()
    user_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id, user_id=user_id)
    query = GetSubscriptionByIdQuery(subscription_id=subscription_id, user_id=uuid4())

    # act
    with pytest.raises(ForbiddenActionException) as e:
        await mediator.handle_query(query)

    # assert
    assert e.value.message == f'Доступ запрещен: невозможно получить чужую подписку'


