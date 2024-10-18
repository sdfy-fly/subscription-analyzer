from uuid import uuid4

from src.application.queries.category.get_user_categories_query import GetUserCategoriesQuery
from src.domain.entity.category import Category


async def test_get_user_categories__ok(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)
    expected_categories_names = [
        'category 1',
        'category 2',
        'category 3',
    ]
    await insert_category(name='category 1', user_id=user_id)
    await insert_category(name='category 2', user_id=user_id)
    await insert_category(name='category 3', user_id=user_id)

    query = GetUserCategoriesQuery(user_id=user_id)

    # act
    categories: list[Category] = await mediator.handle_query(query)

    # assert
    assert [category.name.value for category in categories] == expected_categories_names


async def test_get_user_categories__empty(mediator, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(user_id=user_id)
    query = GetUserCategoriesQuery(user_id=user_id)

    # act
    categories = await mediator.handle_query(query)

    # assert
    assert categories == []
