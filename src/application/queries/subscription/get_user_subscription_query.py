from dataclasses import dataclass
from uuid import UUID

from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.domain.entity.subscription import Subscription
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class GetUserSubscriptionsQuery(BaseQuery):
    user_id: UUID


@dataclass
class GetUserSubscriptionsQueryHandler(BaseQueryHandler):
    uow: UnitOfWork

    async def handle(self, query: GetUserSubscriptionsQuery) -> list[Subscription]:
        async with self.uow:
            subscriptions = await self.uow.subscription_repo.get_user_subscription(query.user_id)

        return subscriptions
