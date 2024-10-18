from uuid import uuid4

import pytest

from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException
from src.application.queries.category.get_category_by_id_query import GetCategoryByIdQuery
from src.domain.entity.category import Category


async def test_get_category_by_id_query__ok(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id, name='category 1')
    query = GetCategoryByIdQuery(category_id=category_id, user_id=user_id)

    # act
    category: Category = await mediator.handle_query(query)

    # assert
    assert category.id == category_id
    assert category.user_id == user_id
    assert category.name.value == 'category 1'


async def test_get_category_by_id_query__category_does_not_exists(mediator):
    # arrange
    category_id = uuid4()
    query = GetCategoryByIdQuery(category_id=category_id, user_id=uuid4())

    # act
    with pytest.raises(CategoryNotFound) as e:
        await mediator.handle_query(query)

    assert e.value.message == f'Категория с id="{category_id}" не найдена!'


async def test_get_category_by_id_query__stranger_category(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    stranger_user_id = uuid4()
    category_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id)
    query = GetCategoryByIdQuery(category_id=category_id, user_id=stranger_user_id)

    # act
    with pytest.raises(ForbiddenActionException) as e:
        await mediator.handle_query(query)

    assert e.value.message == 'Доступ запрещен: невозможно получить чужую категорию'
