from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.commands.category import CreateCategoryCommand, DeleteCategoryCommand, UpdateCategoryCommand
from src.application.exceptions.category import CategoryAlreadyExists, CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException
from src.application.mediator import Mediator
from src.application.queries.category import GetCategoryByIdQuery, GetUserCategoriesQuery
from src.domain.entity.category import Category
from src.presentation.dependencies import get_mediator
from src.presentation.dependencies.auth import get_user_id_by_jwt
from src.presentation.schemas.category import (
    CategorySchema,
    CreateCategoryRequest,
    CreateCategoryResponse,
    UpdateCategoryRequest,
)


router = APIRouter()


@router.post(path='/category', status_code=status.HTTP_201_CREATED, summary='Создает новую категорию')
async def create_category(
    request: CreateCategoryRequest,
    user_id: UUID = Depends(get_user_id_by_jwt),
    mediator: Mediator = Depends(get_mediator),
):
    command = CreateCategoryCommand(name=request.name, user_id=user_id)
    try:
        category: Category = await mediator.handle_command(command)
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message) from e

    return CreateCategoryResponse(id=category.id, name=category.name.value)


@router.get('/{category_id}')
async def get_category_by_id(
    category_id: UUID,
    user_id: UUID = Depends(get_user_id_by_jwt),
    mediator: Mediator = Depends(get_mediator),
) -> CategorySchema:
    query = GetCategoryByIdQuery(category_id=category_id, user_id=user_id)

    try:
        category = await mediator.handle_query(query)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenActionException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

    return CategorySchema.from_entity(category)


@router.get('/')
async def get_user_categories(
    user_id: UUID = Depends(get_user_id_by_jwt),
    mediator: Mediator = Depends(get_mediator),
) -> list[CategorySchema]:
    query = GetUserCategoriesQuery(user_id=user_id)
    categories = await mediator.handle_query(query)
    return [CategorySchema.from_entity(category) for category in categories]


@router.put('/{category_id}')
async def update_category(
    category_id: UUID,
    request: UpdateCategoryRequest,
    user_id: UUID = Depends(get_user_id_by_jwt),
    mediator: Mediator = Depends(get_mediator),
) -> CategorySchema:
    command = UpdateCategoryCommand(category_id=category_id, name=request.name, user_id=user_id)

    try:
        updated_category = await mediator.handle_command(command)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenActionException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return CategorySchema.from_entity(updated_category)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    user_id: UUID = Depends(get_user_id_by_jwt),
    mediator: Mediator = Depends(get_mediator),
):
    command = DeleteCategoryCommand(category_id=category_id, user_id=user_id)

    try:
        await mediator.handle_command(command)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenActionException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
