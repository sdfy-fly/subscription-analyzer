from dataclasses import dataclass
from uuid import UUID

from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.category import CategoryNotFound
from src.application.exceptions.common import ForbiddenActionException
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class DeleteCategoryCommand(BaseCommand):
    category_id: UUID
    user_id: UUID


@dataclass
class DeleteCategoryCommandHandler(BaseCommandHandler):
    uow: UnitOfWork

    async def handle(self, command: DeleteCategoryCommand) -> None:
        async with self.uow:
            category = await self.uow.category_repo.get_by_id(command.category_id)

            if not category:
                raise CategoryNotFound(command.category_id)

            if category.user_id != command.user_id:
                raise ForbiddenActionException('невозможно удалить чужую категорию')

            await self.uow.category_repo.remove(command.category_id)
