from dataclasses import dataclass
from uuid import UUID

from src.domain.entity.user import User
from src.domain.values.user import Email, HashedPassword, Password, Username
from src.infra.repositories.uow import UnitOfWork
from src.infra.security.base import BasePasswordHasher
from src.services.commands.base import BaseCommand, BaseCommandHandler
from src.services.exceptions.user import EmailAlreadyExists, UsernameAlreadyExists


@dataclass(frozen=True)
class RegisterCommand(BaseCommand):
    username: str
    password: str
    email: str | None = None


@dataclass
class RegisterCommandHandler(BaseCommandHandler[UUID]):
    uow: UnitOfWork
    hasher: BasePasswordHasher

    async def handle(self, command: RegisterCommand) -> UUID:
        user = User(
            username=Username(command.username),
            password=Password(command.password),
            email=Email(command.email) if command.email else None,
        )

        async with self.uow:
            if await self.uow.user_repo.is_username_exists(command.username):
                raise UsernameAlreadyExists

            if command.email and await self.uow.user_repo.is_email_exists(command.email):
                raise EmailAlreadyExists

            hashed_password = self.hasher.hash_password(user.password.value)
            user.password = HashedPassword(hashed_password)
            user_id = await self.uow.user_repo.create(user)

        # TODO: выдать jwt токен
        return user_id
