import asyncio
from unittest import mock

import asyncpg
import pytest
from alembic import command
from alembic.config import Config
from asyncpg import Connection
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.mediator import Mediator
from src.core.container import get_container
from src.core.settings import DataBaseSettings
from src.infra.repositories.factories import BaseSessionFactory
from src.presentation.main import create_fastapi_app
from tests.functional.settings import test_settings


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def container():
    return get_container()


@pytest.fixture(scope='session')
def mediator(container) -> Mediator:
    return container.resolve(Mediator)


@pytest.fixture(scope='session', autouse=True)
def mock_pg_dsn():
    with (
        mock.patch.object(DataBaseSettings, 'async_dsn', new=test_settings.db.async_dsn),
        mock.patch.object(DataBaseSettings, 'sync_dsn', new=test_settings.db.sync_dsn),
    ):
        yield


@pytest.fixture(name='pg_session')
async def get_pg_session(mock_pg_dsn, container) -> AsyncSession:
    session_factory: BaseSessionFactory = container.resolve(BaseSessionFactory)
    async with session_factory.get_session() as session:
        yield session


@pytest.fixture(name='pg')
async def get_pg_connection(container) -> Connection:
    connection = await asyncpg.connect(test_settings.db.sync_dsn)
    yield connection
    await connection.close()


@pytest.fixture(autouse=True)
async def apply_migrations():
    alembic_config = Config(str(test_settings.base_dir / 'alembic.ini'))
    alembic_config.set_main_option('script_location', str(test_settings.base_dir / 'migrations'))

    command.downgrade(alembic_config, 'base')
    command.upgrade(alembic_config, 'head')


@pytest.fixture(scope='session')
def app() -> FastAPI:
    application = create_fastapi_app()
    return application


@pytest.fixture()
async def test_client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac
