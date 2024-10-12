from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.domain.entity.subscription import Subscription


@dataclass
class BaseSubscriptionRepository(ABC):
    @abstractmethod
    async def get_user_subscription(self, user_id: UUID) -> list[Subscription]: ...

    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> Subscription | None: ...

    @abstractmethod
    async def is_subscription_exists(self, subscription: Subscription) -> bool: ...

    @abstractmethod
    async def create(self, subscription: Subscription) -> Subscription: ...

    @abstractmethod
    async def update(self, subscription: Subscription) -> Subscription: ...
