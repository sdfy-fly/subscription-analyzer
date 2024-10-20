from uuid import uuid4

import pytest

from src.domain.entity.user import User
from src.domain.repositories.user import BaseUserRepository
from src.domain.values.user import Email, HashedPassword, Username


@pytest.fixture(name='user_repo')
async def get_repo(container, pg_session):
    repo: BaseUserRepository = container.resolve(BaseUserRepository, session=pg_session)
    yield repo


async def test_user__create(user_repo, pg_session, pg):
    # arrange
    user = User(
        username=Username('test user123'),
        password=HashedPassword('password1'),
        email=Email('test123@gmail.com'),
    )

    # act
    await user_repo.create(user)
    await pg_session.commit()

    # assert
    user_from_db = await pg.fetch('SELECT * FROM users')
    assert len(user_from_db) == 1
    user_from_db = user_from_db[0]

    assert user_from_db['id'] == user.id
    assert user_from_db['username'] == user.username.value
    assert user_from_db['password'] == user.password.value
    assert user_from_db['email'] == user.email.value
    assert user_from_db['created_at'] == user.created_at
    assert user_from_db['updated_at'] == user.updated_at


@pytest.mark.parametrize(
    'new_username, existing_username, expected_result',
    [
        ('username1', 'username1', True),
        ('username2', 'username1', False),
    ],
)
async def test_user__is_username_exists(user_repo, pg_session, pg, new_username, existing_username, expected_result):
    # arrange
    user = User(username=Username(existing_username), password=HashedPassword('password1'))

    # act
    await user_repo.create(user)
    result = await user_repo.is_username_exists(new_username)

    # assert
    assert result is expected_result


@pytest.mark.parametrize(
    'new_email, existing_email, expected_result',
    [
        ('username1@gmail.com', 'username1@gmail.com', True),
        ('username2@gmail.com', 'username1@gmail.com', False),
    ],
)
async def test_user__is_email_exists(user_repo, pg_session, pg, new_email, existing_email, expected_result):
    # arrange
    user = User(username=Username('username1'), password=HashedPassword('password1'), email=Email(existing_email))

    # act
    await user_repo.create(user)
    result = await user_repo.is_email_exists(new_email)

    # assert
    assert result is expected_result


async def test_user__get_user_by_username__ok(user_repo, insert_user):
    # arrange
    user_id = uuid4()
    await insert_user(username='username 123', user_id=user_id)

    # act
    user = await user_repo.get_user_by_username('username 123')

    # assert
    assert user.id == user_id
    assert user.username.value == 'username 123'


async def test_user__get_user_by_username__does_not_exists(user_repo):
    # act
    user = await user_repo.get_user_by_username('username 123')

    # assert
    assert user is None
