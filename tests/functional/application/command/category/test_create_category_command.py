from uuid import uuid4

import pytest

from src.domain.entity.category import Category
from src.application.commands.category.create_category_command import CreateCategoryCommand
from src.application.exceptions.category import CategoryAlreadyExists


async def test_create_category_command__ok(mediator, insert_user):
    # arrange
    user_id = uuid4()
    command = CreateCategoryCommand(name='category 1', user_id=user_id)
    await insert_user(user_id=user_id)

    # act
    category: Category = await mediator.handle_command(command)

    assert category is not None
    assert category.name.value == 'category 1'


async def test_create_category_command__already_exists(mediator, insert_user, insert_category):
    # arrange
    user_id = uuid4()
    command = CreateCategoryCommand(name='category 1', user_id=user_id)

    # act
    await insert_user(user_id=user_id)
    await insert_category(user_id=user_id, name='category 1')

    with pytest.raises(CategoryAlreadyExists):
        await mediator.handle_command(command)
