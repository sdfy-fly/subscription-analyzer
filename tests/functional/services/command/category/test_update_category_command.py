from uuid import uuid4

import pytest

from src.domain.entity.category import Category
from src.domain.values.category import Name
from src.services.commands.category.update_category_command import UpdateCategoryCommand
from src.services.exceptions.category import CategoryAlreadyExists
from src.services.exceptions.common import ForbiddenActionException


async def test_update_category_command__ok(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    category = Category(name=Name('category 1'), user_id=user_id)
    command = UpdateCategoryCommand(category_id=category.id, name='updated category', user_id=user_id)
    await insert_user(user_id=user_id)
    await insert_category(category_id=category.id, name=category.name.value, user_id=user_id)

    # act
    updated_category: Category = await mediator.handle_command(command)

    # assert
    assert updated_category.id == category.id
    assert updated_category.name.value == 'updated category'
    assert updated_category.user_id == category.user_id
    assert updated_category.updated_at > category.updated_at


async def test_update_category_command__values_no_changes(mediator, insert_user, insert_category):
    """Тест проверяет кейс когда пользователь обновляет категорию ничего не меняя"""
    # arrange
    user_id = uuid4()
    category = Category(name=Name('category 1'), user_id=user_id)
    command = UpdateCategoryCommand(category_id=category.id, name='category 1', user_id=user_id)
    await insert_user(user_id=user_id)
    await insert_category(category_id=category.id, name=category.name.value, user_id=user_id)

    # act
    updated_category: Category = await mediator.handle_command(command)

    # assert
    assert updated_category.id == category.id
    assert updated_category.name.value == category.name.value
    assert updated_category.user_id == category.user_id
    assert updated_category.updated_at > category.updated_at


async def test_update_category_command__update_stranger_category(mediator, insert_user, insert_category):
    # arrange
    user_id_1 = uuid4()
    user_id_2 = uuid4()
    category_id = uuid4()
    await insert_user(user_id=user_id_1)
    await insert_user(user_id=user_id_2)
    await insert_category(category_id=category_id, name='category 1', user_id=user_id_1)

    # user_2 обновляет категорию пользователя user_1
    command = UpdateCategoryCommand(category_id=category_id, name='updated category', user_id=user_id_2)

    # act
    with pytest.raises(ForbiddenActionException):
        await mediator.handle_command(command)


async def test_update_category__already_exists(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    category_1 = Category(name=Name('category 1'), user_id=user_id)
    category_2 = Category(name=Name('category 2'), user_id=user_id)
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_1.id, name=category_1.name.value, user_id=user_id)
    await insert_category(category_id=category_2.id, name=category_2.name.value, user_id=user_id)

    command = UpdateCategoryCommand(category_id=category_2.id, name='category 1', user_id=user_id)

    # act
    with pytest.raises(CategoryAlreadyExists):
        await mediator.handle_command(command)
