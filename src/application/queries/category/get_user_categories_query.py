from dataclasses import dataclass
from uuid import UUID

from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.domain.entity.category import Category
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class GetUserCategoriesQuery(BaseQuery):
    user_id: UUID


@dataclass
class GetUserCategoriesQueryHandler(BaseQueryHandler[list[Category]]):
    uow: UnitOfWork

    async def handle(self, query: GetUserCategoriesQuery) -> list[Category]:
        async with self.uow:
            categories = await self.uow.category_repo.get_user_categories(query.user_id)

        return categories
