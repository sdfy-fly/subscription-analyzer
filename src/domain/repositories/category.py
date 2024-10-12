from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from src.domain.entity.category import Category


@dataclass
class BaseCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category: ...

    @abstractmethod
    async def get_user_categories(self, user_id: UUID) -> list[Category]: ...

    @abstractmethod
    async def is_category_exists(self, category: Category) -> bool: ...

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category | None: ...

    @abstractmethod
    async def update(self, category: Category) -> Category: ...
