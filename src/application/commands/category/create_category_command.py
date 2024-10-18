from dataclasses import dataclass
from uuid import UUID

from src.domain.entity.category import Category
from src.domain.values.category import Name
from src.infra.repositories.uow import UnitOfWork
from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.category import CategoryAlreadyExists


@dataclass(frozen=True)
class CreateCategoryCommand(BaseCommand):
    name: str
    user_id: UUID


@dataclass
class CreateCategoryCommandHandler(BaseCommandHandler[Category]):
    uow: UnitOfWork

    async def handle(self, command: CreateCategoryCommand) -> Category:
        category = Category(name=Name(command.name), user_id=command.user_id)

        async with self.uow:
            if await self.uow.category_repo.is_category_exists(category):
                raise CategoryAlreadyExists

            await self.uow.category_repo.create(category)

        return category
