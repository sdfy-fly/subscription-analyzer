from uuid import UUID

import pytest

from src.infra.security.base import BaseTokenManager


@pytest.fixture
def get_jwt_token(insert_user, container):
    manager: BaseTokenManager = container.resolve(BaseTokenManager)

    async def wrapper(user_id: UUID, create: bool):
        if create:
            await insert_user(user_id=user_id)

        return manager.create_token(user_id=user_id)

    return wrapper


@pytest.fixture
def get_auth_header(get_jwt_token):
    async def wrapper(user_id: UUID, create: bool = False):
        token = await get_jwt_token(user_id=user_id, create=create)
        return {'Authorization': f'Bearer {token}'}

    return wrapper
