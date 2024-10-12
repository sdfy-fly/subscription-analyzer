from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.settings import settings
from src.infra.repositories.factories import BaseSessionFactory


class Base(DeclarativeBase): ...


class PostgresSessionFactory(BaseSessionFactory):
    def __init__(self):
        self._engine = create_async_engine(url=settings.db.async_dsn, echo=settings.db.show_query)
        self.async_session_maker = async_sessionmaker(self._engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, Any]:
        session: AsyncSession = self.async_session_maker()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
