from datetime import datetime
from typing import cast
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entity.subscription import Subscription
from src.domain.values.subscription import Budget, Cost, Name
from src.infra.repositories.postgres.factories import Base
from src.infra.repositories.postgres.models.category import CategoryModel
from src.infra.repositories.postgres.models.mixins import CreatedUpdatedMixin, UUIDMixin


class SubscriptionModel(UUIDMixin, CreatedUpdatedMixin, Base):
    __tablename__ = 'subscriptions'

    name: Mapped[str]
    cost: Mapped[float]
    budget: Mapped[float] = mapped_column(nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expired_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    notification_on_expire: Mapped[bool]
    notification_on_budget_threshold: Mapped[bool]
    category_id: Mapped[UUID | None] = mapped_column(ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    category: Mapped[CategoryModel] = relationship('CategoryModel', lazy='selectin')

    __table_args__ = (UniqueConstraint('name', 'user_id', name='idx_subscription_name_user_id_uniq'),)

    def to_entity(self) -> Subscription:
        category = CategoryModel.to_entity(cast(CategoryModel, self.category)) if self.category else None
        budget = Budget(cast(float, self.budget)) if self.budget else None

        return Subscription(
            id=self.id,
            name=Name(self.name),
            cost=Cost(self.cost),
            budget=budget,
            start_date=self.start_date,
            expired_date=self.expired_date,
            user_id=self.user_id,
            category=category,
            notification_on_expire=self.notification_on_expire,
            notification_on_budget_threshold=self.notification_on_budget_threshold,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
