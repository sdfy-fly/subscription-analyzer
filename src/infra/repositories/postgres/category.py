from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.category import Category
from src.domain.repositories.category import BaseCategoryRepository
from src.infra.repositories.postgres.models import CategoryModel


@dataclass
class PostgresCategoryRepository(BaseCategoryRepository):
    session: AsyncSession

    # TODO: в команде проверить ошибку на индекс уникальности
    async def create(self, category: Category) -> Category:
        query = (
            insert(CategoryModel)
            .values(
                id=category.id,
                name=category.name.value,
                user_id=category.user_id,
                created_at=category.created_at,
                updated_at=category.updated_at,
            )
            .on_conflict_do_nothing()
            .returning(CategoryModel)
        )

        category = await self.session.scalars(query)
        return CategoryModel.to_entity(category.one_or_none())

    async def is_category_exists(self, category: Category) -> bool:
        query = select(CategoryModel).where(
            and_(
                CategoryModel.user_id == category.user_id,
                CategoryModel.name == category.name.value,
            )
        )
        result = await self.session.scalar(query)
        return result is not None

    async def get_user_categories(self, user_id: UUID) -> list[Category]:
        categories = await self.session.scalars(select(CategoryModel).filter_by(user_id=user_id))

        return [CategoryModel.to_entity(category) for category in categories.all()]

    async def get_by_id(self, category_id: UUID) -> Category | None:
        category = await self.session.scalars(select(CategoryModel).filter_by(id=category_id))

        if not (category := category.one_or_none()):
            return None

        return CategoryModel.to_entity(category)

    # TODO: проверить что я изменяю свою категорию а не чью то еще
    # TODO: отловить ошибку уникальности индекса уникальности (если изменить название на уже существующее)
    async def update(self, category: Category) -> Category:
        query = (
            update(CategoryModel).values(name=category.name.value).filter_by(id=category.id).returning(CategoryModel)
        )
        updated_category = await self.session.scalars(query)

        return CategoryModel.to_entity(updated_category.first())
