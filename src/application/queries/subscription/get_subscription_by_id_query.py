from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.common import ForbiddenActionException
from src.application.exceptions.subscription import SubscriptionNotFound
from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.domain.entity.subscription import Subscription
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class GetSubscriptionByIdQuery(BaseQuery):
    subscription_id: UUID
    user_id: UUID


@dataclass
class GetSubscriptionByIdQueryHandler(BaseQueryHandler):
    uow: UnitOfWork

    async def handle(self, query: GetSubscriptionByIdQuery) -> Subscription:
        async with self.uow:
            subscription = await self.uow.subscription_repo.get_by_id(query.subscription_id)
            if not subscription:
                raise SubscriptionNotFound(query.subscription_id)

            if subscription.user_id != query.user_id:
                raise ForbiddenActionException('невозможно получить чужую подписку')

            return subscription
