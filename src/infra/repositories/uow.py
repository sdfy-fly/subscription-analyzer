from dataclasses import dataclass

from punq import Container

from src.domain.repositories.category import BaseCategoryRepository
from src.domain.repositories.subscription import BaseSubscriptionRepository
from src.domain.repositories.user import BaseUserRepository
from src.infra.repositories.factories import BaseSessionFactory


@dataclass
class UnitOfWork:
    _session_factory: BaseSessionFactory
    _container: Container

    async def __aenter__(self):
        self._session_context = self._session_factory.get_session()
        self._session = await self._session_context.__aenter__()

        self.user_repo: BaseUserRepository = self._container.resolve(BaseUserRepository, session=self._session)
        self.category_repo: BaseCategoryRepository = self._container.resolve(
            BaseCategoryRepository, session=self._session
        )
        self.subscription_repo: BaseSubscriptionRepository = self._container.resolve(
            BaseSubscriptionRepository, session=self._session
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session_context.__aexit__(exc_type, exc_val, exc_tb)
