from uuid import uuid4

import pytest

from src.application.commands.category.delete_category_command import DeleteCategoryCommand
from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException


async def test_delete_category_command__ok(mediator, insert_user, insert_category, pg):
    # arrange
    user_id = uuid4()
    category_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id)
    command = DeleteCategoryCommand(category_id=category_id, user_id=user_id)

    # act
    await mediator.handle_command(command)

    # assert
    assert not await pg.fetch('SELECT * FROM categories')


async def test_delete_category_command__category_does_not_exists(mediator):
    # arrange
    category_id = uuid4()
    command = DeleteCategoryCommand(category_id=category_id, user_id=uuid4())

    # act
    with pytest.raises(CategoryNotFound):
        await mediator.handle_command(command)


async def test_delete_category_command__access_denied(mediator, insert_category, insert_user):
    # arrange
    category_id = uuid4()
    user_id = uuid4()
    await insert_user(user_id=user_id)
    await insert_category(category_id=category_id, user_id=user_id)
    command = DeleteCategoryCommand(category_id=category_id, user_id=uuid4())

    # act
    with pytest.raises(ForbiddenActionException):
        await mediator.handle_command(command)
