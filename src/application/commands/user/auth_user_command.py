from dataclasses import dataclass

from src.application.commands.base import BaseCommand, BaseCommandHandler
from src.application.exceptions.user import AuthException
from src.infra.repositories.uow import UnitOfWork
from src.infra.security.base import BasePasswordHasher, BaseTokenManager


@dataclass(frozen=True)
class AuthUserCommand(BaseCommand):
    username: str
    password: str


@dataclass
class AuthUserCommandHandler(BaseCommandHandler[str]):
    uow: UnitOfWork
    token_manager: BaseTokenManager
    hasher: BasePasswordHasher

    async def handle(self, command: AuthUserCommand) -> str:
        async with self.uow:
            user = await self.uow.user_repo.get_user_by_username(command.username)
            if not user:
                raise AuthException('Неверный логин или пароль!')

            if not self.hasher.verify_password(command.password, user.password.value):
                raise AuthException('Неверный логин или пароль!')

            return self.token_manager.create_token(user.id)
