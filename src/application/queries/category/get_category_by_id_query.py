from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException
from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.domain.entity.category import Category
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class GetCategoryByIdQuery(BaseQuery):
    category_id: UUID
    user_id: UUID


@dataclass
class GetCategoryByIdQueryHandler(BaseQueryHandler[Category]):
    uow: UnitOfWork

    async def handle(self, query: GetCategoryByIdQuery) -> Category:
        async with self.uow:
            category = await self.uow.category_repo.get_by_id(query.category_id)

            if not category:
                raise CategoryNotFound(query.category_id)

            if category.user_id != query.user_id:
                raise ForbiddenActionException('невозможно получить чужую категорию')

            return category
