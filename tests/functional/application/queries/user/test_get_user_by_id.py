from uuid import uuid4

import pytest

from src.application.exceptions.user import UserNotFound
from src.application.queries.user.get_user_by_id_query import GetUserByIdQuery
from src.domain.entity.user import User


async def test_get_user_by_id__ok(mediator, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id, username='user 1')
    query = GetUserByIdQuery(user_id=user_id)

    # act
    user: User = await mediator.handle_query(query)

    # assert
    assert user.id == user_id
    assert user.username.value == 'user 1'


async def test_get_user_by_id__not_found(mediator):
    # arrange
    user_id = uuid4()
    query = GetUserByIdQuery(user_id=user_id)

    # act
    with pytest.raises(UserNotFound) as e:
        await mediator.handle_query(query)

    # assert
    assert e.value.message == f'Пользователя с id="{user_id}" не найден!'
