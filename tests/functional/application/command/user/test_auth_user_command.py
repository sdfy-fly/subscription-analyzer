import pytest

from src.application.commands.user import RegisterCommand
from src.application.commands.user.auth_user_command import AuthUserCommand
from src.application.exceptions.user import AuthException
from src.infra.security.base import BaseTokenManager


@pytest.fixture
def token_manager(container) -> BaseTokenManager:
    return container.resolve(BaseTokenManager)


async def test_auth_user_command__ok(mediator, container, pg, token_manager):
    # arrange
    register_command = RegisterCommand(username='username', password='Password123!')
    await mediator.handle_command(register_command)
    user_id = await pg.fetchval('SELECT id from users;')

    # act
    auth_command = AuthUserCommand(username='username', password='Password123!')
    token = await mediator.handle_command(auth_command)

    # assert
    assert token_manager.verify_token(token) == user_id


async def test_auth_user_command__username_does_not_exists(mediator, container, insert_user):
    # arrange
    auth_command = AuthUserCommand(username='username', password='123')

    # act
    with pytest.raises(AuthException) as e:
        await mediator.handle_command(auth_command)

    # assert
    assert e.value.message == 'Неверный логин или пароль!'


async def test_auth_user_command__wrong_password(mediator, insert_user):
    # arrange
    register_command = RegisterCommand(username='username', password='Correct_Password123')
    await mediator.handle_command(register_command)

    # act
    auth_command = AuthUserCommand(username='username', password='wrong_password')
    with pytest.raises(AuthException):
        await mediator.handle_command(auth_command)
