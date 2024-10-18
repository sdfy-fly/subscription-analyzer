from dataclasses import dataclass
from uuid import UUID

from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.category import CategoryAlreadyExists, CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException
from src.domain.entity.category import Category
from src.domain.values.category import Name
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class UpdateCategoryCommand(BaseCommand):
    category_id: UUID
    name: str
    user_id: UUID


@dataclass
class UpdateCategoryCommandHandler(BaseCommandHandler[Category]):
    uow: UnitOfWork

    async def handle(self, command: UpdateCategoryCommand) -> Category:
        category_to_update = Category(id=command.category_id, name=Name(command.name), user_id=command.user_id)

        async with self.uow:
            category = await self.uow.category_repo.get_by_id(command.category_id)
            if not category:
                raise CategoryNotFound(command.category_id)

            if category.user_id != command.user_id:
                raise ForbiddenActionException('нельзя обновить чужую категорию')

            if await self.uow.category_repo.is_category_exists(category_to_update):
                raise CategoryAlreadyExists

            updated_category = await self.uow.category_repo.update(category_to_update)

        return updated_category
