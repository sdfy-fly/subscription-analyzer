from functools import lru_cache

import punq

from src.domain.repositories.category import BaseCategoryRepository
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.factories import BaseSessionFactory
from src.infra.repositories.postgres.category import PostgresCategoryRepository
from src.infra.repositories.postgres.factories import PostgresSessionFactory
from src.infra.repositories.postgres.subscription import PostgresSubscriptionRepository
from src.infra.repositories.postgres.user import PostgresUserRepository


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    # Session Factory
    container.register(BaseSessionFactory, PostgresSessionFactory, scope=punq.Scope.singleton)

    # Repository
    container.register(BaseUserRepository, PostgresUserRepository)
    container.register(BaseCategoryRepository, PostgresCategoryRepository)
    container.register(BaseSubscriptionRepository, PostgresSubscriptionRepository)

    return container
