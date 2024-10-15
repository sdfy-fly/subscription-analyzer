import pytest

from src.infra.security.base import BasePasswordHasher


@pytest.fixture()
def hasher(container) -> BasePasswordHasher:
    return container.resolve(BasePasswordHasher)


@pytest.mark.parametrize(
    'password',
    [
        'password123',
        'пароль123',
        'Password!123',
    ],
)
async def test_password__hash(hasher, password):
    # act
    hashed_password = hasher.hash_password(password)

    # assert
    assert hasher.verify_password(password=password, hashed_password=hashed_password)
