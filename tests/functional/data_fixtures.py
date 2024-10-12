from uuid import UUID, uuid4

import faker
import pytest

from src.domain.helpers import get_utc_now
from src.infra.repositories.postgres.models import CategoryModel, UserModel


faker_ = faker.Faker()


@pytest.fixture
def insert_user(pg):
    async def wrapper(
        user_id: UUID | None = None, username: str | None = None, password: str | None = None, email: str | None = None
    ):
        user_id = user_id if user_id else uuid4()
        username = username if username else faker_.user_name()
        password = password if password else faker_.password()
        email = email if email else faker_.email()
        created_updated_ts = get_utc_now()
        await pg.copy_records_to_table(
            table_name=UserModel.__tablename__,
            columns=['id', 'username', 'password', 'email', 'created_at', 'updated_at'],
            records=[(user_id, username, password, email, created_updated_ts, created_updated_ts)],
        )

    return wrapper


@pytest.fixture
def insert_category(pg):
    async def wrapper(user_id: UUID, category_id: UUID | None = None, name: str | None = None):
        category_id = category_id if category_id else uuid4()
        name = name if name else faker_.name()
        created_updated_ts = get_utc_now()
        await pg.copy_records_to_table(
            table_name=CategoryModel.__tablename__,
            columns=['id', 'name', 'user_id', 'created_at', 'updated_at'],
            records=[(category_id, name, user_id, created_updated_ts, created_updated_ts)],
        )

    return wrapper
