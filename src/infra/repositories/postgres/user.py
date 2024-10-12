from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.user import User
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.postgres.models import UserModel


@dataclass
class PostgresUserRepository(BaseUserRepository):
    session: AsyncSession

    # TODO: в команде проверить ошибки индекса уникальности
    # TODO: хешировать пароль
    async def create(self, user: User) -> User:
        email = user.email.value if user.email else None
        query = (
            insert(UserModel)
            .values(
                id=user.id,
                username=user.username.value,
                password=user.password.value,
                email=email,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            .returning(UserModel)
        )

        user = await self.session.scalars(query)
        return UserModel.to_entity(user.one_or_none())

    async def is_username_exists(self, username: str) -> bool:
        query = select(UserModel.id).filter_by(username=username)
        result = await self.session.scalar(query)
        return result is not None

    async def is_email_exists(self, email: str) -> bool:
        query = select(UserModel.id).filter_by(email=email)
        result = await self.session.scalar(query)
        return result is not None
