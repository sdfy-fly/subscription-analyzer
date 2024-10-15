from dataclasses import dataclass

from punq import Container

from src.domain.repositories.category import BaseCategoryRepository
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.factories import BaseSessionFactory


@dataclass
class UnitOfWork:
    session_factory: BaseSessionFactory
    container: Container

    async def __aenter__(self):
        self.session_context = self.session_factory.get_session()
        self.session = await self.session_context.__aenter__()

        self.user_repo: BaseUserRepository = self.container.resolve(BaseUserRepository, session=self.session)
        self.category_repo: BaseCategoryRepository = self.container.resolve(
            BaseCategoryRepository, session=self.session
        )
        self.subscription_repo: BaseSubscriptionRepository = self.container.resolve(
            BaseSubscriptionRepository, session=self.session
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session_context.__aexit__(exc_type, exc_val, exc_tb)
