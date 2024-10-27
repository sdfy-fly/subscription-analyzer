import pytest

from src.application.commands.user.register_command import RegisterCommand
from src.application.exceptions.user import EmailAlreadyExists, UsernameAlreadyExists
from src.infra.security.base import BasePasswordHasher, BaseTokenManager


async def test_register_command__ok(mediator, container, pg):
    # arrange
    password = 'Password123!'
    command = RegisterCommand(username='username1', password=password, email=None)
    hasher: BasePasswordHasher = container.resolve(BasePasswordHasher)
    token_manager: BaseTokenManager = container.resolve(BaseTokenManager)

    # act
    token = await mediator.handle_command(command)

    # assert
    user_in_db = await pg.fetchrow('SELECT * FROM users')
    user_id = token_manager.verify_token(token)
    assert user_in_db['id'] == user_id
    assert user_in_db['password'] != password
    assert hasher.verify_password(password, user_in_db['password'])


async def test_register_command__username_already_exists(mediator, insert_user):
    # arrange
    command = RegisterCommand(username='username1', password='Password123!', email=None)
    await insert_user(username='username1')

    # act
    with pytest.raises(UsernameAlreadyExists):
        await mediator.handle_command(command)


async def test_register_command__email_already_exists(mediator, insert_user):
    # arrange
    command = RegisterCommand(username='username1', password='Password123!', email='test@gmail.com')
    await insert_user(email='test@gmail.com')

    # act
    with pytest.raises(EmailAlreadyExists):
        await mediator.handle_command(command)
