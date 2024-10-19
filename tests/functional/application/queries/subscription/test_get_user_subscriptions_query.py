from uuid import uuid4

from src.application.queries.subscription.get_user_subscription_query import GetUserSubscriptionsQuery


async def test_get_user_subscription_query__ok(mediator, insert_user, insert_subscription):
    # arrange
    user_id = uuid4()
    subscription_id_1 = uuid4()
    subscription_id_2 = uuid4()
    subscription_id_3 = uuid4()
    expected_subscriptions_ids = [subscription_id_1, subscription_id_2, subscription_id_3]
    await insert_user(user_id=user_id)
    await insert_subscription(subscription_id=subscription_id_1, user_id=user_id)
    await insert_subscription(subscription_id=subscription_id_2, user_id=user_id)
    await insert_subscription(subscription_id=subscription_id_3, user_id=user_id)
    query = GetUserSubscriptionsQuery(user_id=user_id)

    # act
    subscriptions = await mediator.handle_query(query)

    # assert
    assert [subscription.id for subscription in subscriptions] == expected_subscriptions_ids


async def test_get_user_subscription_query__empty(mediator, insert_user):
    # arrange
    user_id = uuid4()
    query = GetUserSubscriptionsQuery(user_id=user_id)

    # act
    subscriptions = await mediator.handle_query(query)

    # assert
    assert subscriptions == []
