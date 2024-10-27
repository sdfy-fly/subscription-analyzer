from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.entity.category import Category


class CategorySchema(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, category: Category):
        return cls(
            id=category.id, name=category.name.value, created_at=category.created_at, updated_at=category.updated_at
        )


class CreateCategoryRequest(BaseModel):
    name: str


class CreateCategoryResponse(BaseModel):
    id: UUID
    name: str


class GetCategoryByIdResponse(BaseModel):
    category: CategorySchema

    @classmethod
    def from_entity(cls, category: Category):
        return cls(category=CategorySchema.from_entity(category))


class GetUserCategoriesResponse(BaseModel):
    categories: list[CategorySchema]

    @classmethod
    def from_entity(cls, categories: list[Category]):
        _categories = [CategorySchema.from_entity(category) for category in categories]
        return cls(categories=_categories)


class UpdateCategoryRequest(BaseModel):
    name: str


class UpdateCategoryResponse(BaseModel):
    category: CategorySchema
