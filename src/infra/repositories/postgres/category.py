from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import and_, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.category import Category
from src.domain.repositories.category import BaseCategoryRepository
from src.infra.repositories.postgres.models import CategoryModel


@dataclass
class PostgresCategoryRepository(BaseCategoryRepository):
    session: AsyncSession

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
            .returning(CategoryModel)
        )

        category = await self.session.scalars(query)
        return CategoryModel.to_entity(category.one_or_none())

    async def is_category_exists(self, category: Category) -> bool:
        query = select(CategoryModel.id).where(
            and_(
                CategoryModel.id != category.id,
                CategoryModel.user_id == category.user_id,
                CategoryModel.name == category.name.value,
            )
        )
        result = await self.session.scalar(query)
        return result is not None

    async def get_user_categories(self, user_id: UUID) -> list[Category]:
        query = select(CategoryModel).filter_by(user_id=user_id)
        categories = await self.session.scalars(query)
        return [CategoryModel.to_entity(category) for category in categories.all()]

    async def get_by_id(self, category_id: UUID) -> Category | None:
        query = select(CategoryModel).filter_by(id=category_id)
        category = await self.session.scalar(query)
        return CategoryModel.to_entity(category) if category else None

    async def update(self, category: Category) -> Category:
        query = (
            update(CategoryModel).values(name=category.name.value).filter_by(id=category.id).returning(CategoryModel)
        )
        updated_category = await self.session.scalars(query)

        return CategoryModel.to_entity(updated_category.first())

    async def remove(self, category_id: UUID) -> None:
        query = delete(CategoryModel).filter_by(id=category_id)
        await self.session.execute(query)
