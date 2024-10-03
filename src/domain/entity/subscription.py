from dataclasses import dataclass
from datetime import datetime

from src.domain.entity.base import BaseEntity
from src.domain.entity.category import Category
from src.domain.values.subscription import Name, SubscriptionId, Cost


@dataclass(kw_only=True)
class Subscription(BaseEntity):
    id: SubscriptionId
    """Id подписки"""
    name: Name
    """Название подписки"""
    category: Category
    """Категория"""
    cost: Cost
    """Ежемесячная стоимость"""
    start_date: datetime
    """Дата начала подписки"""
    expired_date: datetime
    """Дата истечения подписки"""
    notification_on_expire: bool
    """Уведомлять о истечении подписки"""
    notification_on_budget_threshold: bool
    """Уведомлять о превышении бюджета"""


@dataclass
class SubscriptionAnalytics:
    ...

