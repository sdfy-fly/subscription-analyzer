from uuid import uuid4

import pytest
from freezegun import freeze_time

from src.infra.exceptions.security import InvalidJwt
from src.infra.security.base import BaseTokenManager


@pytest.fixture
def manager(container) -> BaseTokenManager:
    return container.resolve(BaseTokenManager)


@freeze_time('2023-01-01 12:00:00')
def test_token__full_flow__ok(manager):
    # arrange
    user_id = uuid4()

    # act
    token = manager.create_token(user_id)
    verified = manager.verify_token(token)

    # assert
    assert token is not None
    assert verified == user_id


def test_token__expired(manager):
    # arrange
    user_id = uuid4()

    with freeze_time('2000-01-01'):
        token = manager.create_token(user_id)

    # act
    with freeze_time('2000-01-08'), pytest.raises(InvalidJwt):
        manager.verify_token(token)


@pytest.mark.parametrize(
    'token',
    [
        'invalid.token.format',
        '123',
        'asfdasf123',
    ],
)
def test_token___invalid_token(manager, token):
    # act
    with pytest.raises(InvalidJwt):
        manager.verify_token(token)
