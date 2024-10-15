from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.entity.subscription import Subscription
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.infra.repositories.postgres.models import SubscriptionModel


@dataclass
class PostgresSubscriptionRepository(BaseSubscriptionRepository):
    session: AsyncSession

    async def get_user_subscription(self, user_id: UUID) -> list[Subscription]:
        query = select(SubscriptionModel).filter_by(user_id=user_id).options(joinedload(SubscriptionModel.category))
        result = await self.session.scalars(query)

        return [SubscriptionModel.to_entity(subscription) for subscription in result.unique().all()]

    async def get_by_id(self, subscription_id: UUID) -> Subscription | None:
        query = select(SubscriptionModel).filter_by(id=subscription_id).options(joinedload(SubscriptionModel.category))

        result = await self.session.scalars(query)
        if not (subscription := result.unique().one_or_none()):
            return None

        return SubscriptionModel.to_entity(subscription)

    async def is_subscription_exists(self, subscription: Subscription) -> bool:
        query = select(SubscriptionModel).where(
            and_(SubscriptionModel.name == subscription.name.value, SubscriptionModel.user_id == subscription.user_id)
        )

        result = await self.session.scalar(query)
        return result is not None

    async def create(self, subscription: Subscription) -> Subscription:
        budget = subscription.budget.value if subscription.budget else None
        category_id = subscription.category.id if subscription.category else None
        query = (
            insert(SubscriptionModel)
            .values(
                id=subscription.id,
                name=subscription.name.value,
                cost=subscription.cost.value,
                budget=budget,
                start_date=subscription.start_date,
                expired_date=subscription.expired_date,
                notification_on_expire=subscription.notification_on_expire,
                notification_on_budget_threshold=subscription.notification_on_budget_threshold,
                category_id=category_id,
                user_id=subscription.user_id,
                created_at=subscription.created_at,
                updated_at=subscription.updated_at,
            )
            .returning(SubscriptionModel)
        )

        subscription = await self.session.scalars(query)
        return SubscriptionModel.to_entity(subscription.one_or_none())

    async def update(self, subscription: Subscription) -> Subscription:
        budget = subscription.budget.value if subscription.budget else None
        category_id = subscription.category.id if subscription.category else None

        query = (
            update(SubscriptionModel)
            .values(
                name=subscription.name.value,
                cost=subscription.cost.value,
                budget=budget,
                start_date=subscription.start_date,
                expired_date=subscription.expired_date,
                notification_on_expire=subscription.notification_on_expire,
                notification_on_budget_threshold=subscription.notification_on_budget_threshold,
                category_id=category_id,
            )
            .filter_by(id=subscription.id)
            .returning(SubscriptionModel)
        )

        subscription = await self.session.scalars(query)
        return SubscriptionModel.to_entity(subscription.first())
