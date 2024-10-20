from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.user import User
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.postgres.models import UserModel


@dataclass
class PostgresUserRepository(BaseUserRepository):
    session: AsyncSession

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(UserModel).filter_by(id=user_id)
        if not (user := await self.session.scalar(query)):
            return None

        return UserModel.to_entity(user)

    async def create(self, user: User) -> UUID:
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
            .returning(UserModel.id)
        )

        user_id = await self.session.scalar(query)
        return user_id

    async def is_username_exists(self, username: str) -> bool:
        query = select(UserModel.id).filter_by(username=username)
        result = await self.session.scalar(query)
        return result is not None

    async def is_email_exists(self, email: str) -> bool:
        query = select(UserModel.id).filter_by(email=email)
        result = await self.session.scalar(query)
        return result is not None

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(UserModel).filter_by(username=username)
        result = await self.session.scalar(query)
        return UserModel.to_entity(result) if result else None
