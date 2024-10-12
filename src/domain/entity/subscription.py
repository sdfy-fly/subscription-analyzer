from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.domain.entity.base import BaseEntity
from src.domain.entity.category import Category
from src.domain.values.subscription import Budget, Cost, Name


@dataclass(kw_only=True)
class Subscription(BaseEntity):
    id: UUID = field(default_factory=uuid4)
    """Id подписки"""
    name: Name
    """Название подписки"""
    cost: Cost
    """Ежемесячная стоимость"""
    start_date: datetime
    """Дата начала подписки"""
    expired_date: datetime
    """Дата истечения подписки"""
    user_id: UUID
    """Id пользователя"""
    category: Category | None = None
    """Категория"""
    budget: Budget | None = None
    """Выделенный бюджет на подписку"""
    notification_on_expire: bool = False
    """Уведомлять о истечении подписки"""
    notification_on_budget_threshold: bool = False
    """Уведомлять о превышении бюджета"""
