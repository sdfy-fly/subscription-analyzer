from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.subscription import SubscriptionAlreadyExists
from src.domain.entity.category import Category
from src.domain.entity.subscription import Subscription
from src.domain.values.subscription import Budget, Cost, Name
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class UpdateSubscriptionCommand(BaseCommand):
    subscription_id: UUID
    name: str
    cost: float
    start_date: datetime
    expired_date: datetime
    category_id: UUID | None
    user_id: UUID
    budget: float | None
    notification_on_expire: bool
    notification_on_budget_threshold: bool


@dataclass
class UpdateSubscriptionCommandHandler(BaseCommandHandler[Subscription]):
    uow: UnitOfWork

    async def handle(self, command: UpdateSubscriptionCommand) -> Subscription:
        async with self.uow:
            category = await self._get_category_if_exists(command.category_id)
            subscription = Subscription(
                id=command.subscription_id,
                name=Name(command.name),
                cost=Cost(command.cost),
                start_date=command.start_date,
                expired_date=command.expired_date,
                user_id=command.user_id,
                category=category,
                budget=Budget(command.budget) if command.budget else None,
                notification_on_expire=command.notification_on_expire,
                notification_on_budget_threshold=command.notification_on_budget_threshold,
            )

            if await self.uow.subscription_repo.is_subscription_exists(subscription):
                raise SubscriptionAlreadyExists

            subscription = await self.uow.subscription_repo.update(subscription)

        return subscription

    async def _get_category_if_exists(self, category_id: UUID | None) -> Category | None:
        if not category_id:
            return None

        category = await self.uow.category_repo.get_by_id(category_id)
        if not category:
            raise CategoryNotFound(category_id)

        return category
