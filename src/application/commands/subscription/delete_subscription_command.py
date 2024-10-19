from dataclasses import dataclass
from uuid import UUID

from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.common import ForbiddenActionException
from src.application.exceptions.subscription import SubscriptionNotFound
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class DeleteSubscriptionCommand(BaseCommand):
    subscription_id: UUID
    user_id: UUID


@dataclass
class DeleteSubscriptionCommandHandler(BaseCommandHandler):
    uow: UnitOfWork

    async def handle(self, command: DeleteSubscriptionCommand) -> None:
        async with self.uow:
            subscription = await self.uow.subscription_repo.get_by_id(command.subscription_id)

            if not subscription:
                raise SubscriptionNotFound(command.subscription_id)

            if subscription.user_id != command.user_id:
                raise ForbiddenActionException('невозможно удалить чужую подписку')

            await self.uow.subscription_repo.remove(command.subscription_id)
