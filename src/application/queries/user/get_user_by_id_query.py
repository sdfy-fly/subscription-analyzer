from dataclasses import dataclass
from uuid import UUID

from src.application.exceptions.user import UserNotFound
from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.domain.entity.user import User
from src.infra.repositories.uow import UnitOfWork


@dataclass(frozen=True)
class GetUserByIdQuery(BaseQuery):
    user_id: UUID


@dataclass
class GetUserByIdQueryHandler(BaseQueryHandler[User | None]):
    uow: UnitOfWork

    async def handle(self, query: GetUserByIdQuery) -> User:
        async with self.uow:
            user = await self.uow.user_repo.get_user_by_id(query.user_id)
            if not user:
                raise UserNotFound(query.user_id)

        return user
