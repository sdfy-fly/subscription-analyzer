from functools import lru_cache

import punq

from src.application.commands.category.create_category_command import (
    CreateCategoryCommand,
    CreateCategoryCommandHandler,
)
from src.application.commands.category.delete_category_command import (
    DeleteCategoryCommand,
    DeleteCategoryCommandHandler,
)
from src.application.commands.category.update_category_command import (
    UpdateCategoryCommand,
    UpdateCategoryCommandHandler,
)
from src.application.commands.subscription.create_subscription_command import (
    CreateSubscriptionCommand,
    CreateSubscriptionCommandHandler,
)
from src.application.commands.subscription.delete_subscription_command import (
    DeleteSubscriptionCommand,
    DeleteSubscriptionCommandHandler,
)
from src.application.commands.subscription.update_subscription_command import (
    UpdateSubscriptionCommand,
    UpdateSubscriptionCommandHandler,
)
from src.application.commands.user.auth_user_command import AuthUserCommand, AuthUserCommandHandler
from src.application.commands.user.register_command import RegisterCommand, RegisterCommandHandler
from src.application.mediator import Mediator
from src.application.queries.category.get_category_by_id_query import GetCategoryByIdQuery, GetCategoryByIdQueryHandler
from src.application.queries.category.get_user_categories_query import (
    GetUserCategoriesQuery,
    GetUserCategoriesQueryHandler,
)
from src.application.queries.subscription.get_subscription_by_id_query import (
    GetSubscriptionByIdQuery,
    GetSubscriptionByIdQueryHandler,
)
from src.application.queries.subscription.get_user_subscription_query import (
    GetUserSubscriptionsQuery,
    GetUserSubscriptionsQueryHandler,
)
from src.application.queries.user.get_user_by_id_query import GetUserByIdQuery, GetUserByIdQueryHandler
from src.domain.repositories.category import BaseCategoryRepository
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.factories import BaseSessionFactory
from src.infra.repositories.postgres.category import PostgresCategoryRepository
from src.infra.repositories.postgres.factories import PostgresSessionFactory
from src.infra.repositories.postgres.subscription import PostgresSubscriptionRepository
from src.infra.repositories.postgres.user import PostgresUserRepository
from src.infra.repositories.uow import UnitOfWork
from src.infra.security.base import BasePasswordHasher, BaseTokenManager
from src.infra.security.password import PasswordHasher
from src.infra.security.token import JwtTokenManager


@lru_cache(1)
def get_container() -> punq.Container:
    return _init_container()


def _init_container() -> punq.Container:
    container = punq.Container()

    # Security
    container.register(BasePasswordHasher, PasswordHasher)
    container.register(BaseTokenManager, JwtTokenManager)

    # Factories
    container.register(BaseSessionFactory, PostgresSessionFactory, scope=punq.Scope.singleton)

    # Repository
    container.register(BaseUserRepository, PostgresUserRepository)
    container.register(BaseCategoryRepository, PostgresCategoryRepository)
    container.register(BaseSubscriptionRepository, PostgresSubscriptionRepository)

    # Command Handlers
    container.register(RegisterCommandHandler)
    container.register(AuthUserCommandHandler)
    container.register(CreateCategoryCommandHandler)
    container.register(UpdateCategoryCommandHandler)
    container.register(DeleteCategoryCommandHandler)
    container.register(CreateSubscriptionCommandHandler)
    container.register(UpdateSubscriptionCommandHandler)
    container.register(DeleteSubscriptionCommandHandler)

    # Query Handlers
    container.register(GetCategoryByIdQueryHandler)
    container.register(GetUserCategoriesQueryHandler)
    container.register(GetUserByIdQueryHandler)
    container.register(GetSubscriptionByIdQueryHandler)
    container.register(GetUserSubscriptionsQueryHandler)

    # Mediator
    def init_mediator():
        mediator = Mediator()

        # Commands
        # user
        mediator.register_command(command=RegisterCommand, handler=container.resolve(RegisterCommandHandler))
        mediator.register_command(command=AuthUserCommand, handler=container.resolve(AuthUserCommandHandler))
        # category
        mediator.register_command(
            command=CreateCategoryCommand, handler=container.resolve(CreateCategoryCommandHandler)
        )
        mediator.register_command(
            command=UpdateCategoryCommand, handler=container.resolve(UpdateCategoryCommandHandler)
        )
        mediator.register_command(
            command=DeleteCategoryCommand, handler=container.resolve(DeleteCategoryCommandHandler)
        )
        # subscription
        mediator.register_command(
            command=CreateSubscriptionCommand, handler=container.resolve(CreateSubscriptionCommandHandler)
        )
        mediator.register_command(
            command=UpdateSubscriptionCommand, handler=container.resolve(UpdateSubscriptionCommandHandler)
        )
        mediator.register_command(
            command=DeleteSubscriptionCommand, handler=container.resolve(DeleteSubscriptionCommandHandler)
        )

        # Queries
        # user
        mediator.register_query(query=GetUserByIdQuery, handler=container.resolve(GetUserByIdQueryHandler))
        # category
        mediator.register_query(query=GetCategoryByIdQuery, handler=container.resolve(GetCategoryByIdQueryHandler))
        mediator.register_query(query=GetUserCategoriesQuery, handler=container.resolve(GetUserCategoriesQueryHandler))
        # subscription
        mediator.register_query(
            query=GetSubscriptionByIdQuery, handler=container.resolve(GetSubscriptionByIdQueryHandler)
        )
        mediator.register_query(
            query=GetUserSubscriptionsQuery, handler=container.resolve(GetUserSubscriptionsQueryHandler)
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    # UnitOfWork
    container.register(UnitOfWork, container=container)

    return container
