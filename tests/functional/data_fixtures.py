import random
from datetime import datetime
from uuid import UUID, uuid4

import faker
import pytest

from src.domain.helpers import get_utc_now
from src.infra.repositories.postgres.models import CategoryModel, SubscriptionModel, UserModel


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
    async def wrapper(
        user_id: UUID,
        category_id: UUID | None = None,
        name: str | None = None,
        created_updated_ts: datetime | None = None,
    ):
        category_id = category_id if category_id else uuid4()
        name = name if name else faker_.name()
        created_updated_ts = created_updated_ts if created_updated_ts else get_utc_now()
        await pg.copy_records_to_table(
            table_name=CategoryModel.__tablename__,
            columns=['id', 'name', 'user_id', 'created_at', 'updated_at'],
            records=[(category_id, name, user_id, created_updated_ts, created_updated_ts)],
        )

    return wrapper


@pytest.fixture
def insert_subscription(pg):
    async def wrapper(
        user_id: UUID,
        subscription_id: UUID | None = None,
        category_id: UUID | None = None,
        name: str | None = None,
        cost: float | None = None,
        budget: float | None = None,
        start_date: datetime | None = None,
        expired_date: datetime | None = None,
        notification_on_expire: bool = False,
        notification_on_budget_threshold: bool = False,
    ):
        subscription_id = subscription_id if subscription_id else uuid4()
        name = name if name else faker_.name()
        cost = cost if cost else random.randint(1, 1000)
        budget = budget if budget else random.randint(1, 1000)
        start_date = start_date if start_date else get_utc_now()
        expired_date = expired_date if expired_date else get_utc_now()
        created_updated_ts = get_utc_now()
        await pg.copy_records_to_table(
            table_name=SubscriptionModel.__tablename__,
            columns=[
                'id',
                'name',
                'cost',
                'budget',
                'start_date',
                'expired_date',
                'notification_on_expire',
                'notification_on_budget_threshold',
                'category_id',
                'user_id',
                'created_at',
                'updated_at',
            ],
            records=[
                (
                    subscription_id,
                    name,
                    cost,
                    budget,
                    start_date,
                    expired_date,
                    notification_on_expire,
                    notification_on_budget_threshold,
                    category_id,
                    user_id,
                    created_updated_ts,
                    created_updated_ts,
                )
            ],
        )

    return wrapper
