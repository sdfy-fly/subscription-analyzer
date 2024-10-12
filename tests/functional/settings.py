from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class TestDataBaseSettings(BaseSettings):
    user: str = Field(alias='TEST_DB_USER')
    password: str = Field(alias='TEST_DB_PASSWORD')
    host: str = Field(alias='TEST_DB_HOST')
    port: int = Field(alias='TEST_DB_PORT')
    database: str = Field(alias='TEST_DB_NAME')

    @property
    def async_dsn(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

    @property
    def sync_dsn(self):
        return f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


class TestSettings(BaseSettings):
    db: TestDataBaseSettings = TestDataBaseSettings()
    base_dir: Path = Path(__file__).parent.parent.parent.resolve()


test_settings = TestSettings()
