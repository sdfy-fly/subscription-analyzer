import binascii

import pytest

from src.application.commands.user.register_command import RegisterCommand
from src.application.exceptions.user import EmailAlreadyExists, UsernameAlreadyExists
from src.infra.security.base import BasePasswordHasher, BaseTokenManager


async def test_register_command__ok(mediator, container, pg):
    # arrange
    user_password = 'Password123!'
    command = RegisterCommand(username='username1', password=user_password, email=None)
    hasher: BasePasswordHasher = container.resolve(BasePasswordHasher)
    token_manager: BaseTokenManager = container.resolve(BaseTokenManager)

    # act
    token = await mediator.handle_command(command)

    # assert
    user_in_db = await pg.fetch('SELECT * FROM users')
    assert len(user_in_db) == 1
    user_in_db = user_in_db[0]

    user_id = token_manager.verify_token(token)
    assert user_in_db['id'] == user_id
    db_password_bytes = binascii.unhexlify(user_in_db['password'][2:])
    assert hasher.verify_password(user_password, db_password_bytes)


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
