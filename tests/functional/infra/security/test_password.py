import pytest

from src.infra.security.base import BasePasswordHasher


@pytest.fixture()
def hasher(container) -> BasePasswordHasher:
    return container.resolve(BasePasswordHasher)


async def test_password__hash(hasher):
    # arrange
    password = 'Password123!'

    # act
    hashed_password = hasher.hash_password(password)

    # assert
    assert hasher.verify_password(password=password, hashed_password=hashed_password)
