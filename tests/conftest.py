import pytest
from httpx import AsyncClient
from pydantic_settings import SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from src.config import Config, DatabaseConfig
from src.models import Base
from src.main import app
from src.services.database.session import get_async_session

pytest_plugins = []


class TestDatabaseConfig(DatabaseConfig):
    sync_driver: str = "postgresql"

    model_config = SettingsConfigDict(
        env_prefix="TEST_" + DatabaseConfig.model_config["env_prefix"]
    )


class TestConfig(Config):
    database: TestDatabaseConfig = TestDatabaseConfig()

    @property
    def sync_database_url(self) -> str:
        current_driver = self.database.driver
        self.database.driver = self.database.sync_driver

        sync_db_url = self.database_url

        self.database.driver = current_driver

        return sync_db_url


@pytest.fixture(scope="session")
def test_config() -> TestConfig:
    return TestConfig()


@pytest.fixture(scope="session", autouse=True)
async def engine(test_config):
    engine = create_async_engine(test_config.database_url)

    if not database_exists(engine.url):
        create_database(engine.url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()
    drop_database(engine.url)


# @pytest.fixture(scope="session")
# async def db_engine():
#     # Создаем тестовую БД если она не существует
#     # url = make_url(TEST_DATABASE_URL)
#     # if database_exists(url):
#     #     drop_database(url)
#     # create_database(url)
#
#     engine = create_async_engine(TEST_DATABASE_URL)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield engine
#
#     # Удаляем тестовую БД после завершения тестов
#     await engine.dispose()
#     drop_database(url)


# @pytest.fixture(scope="session")
# def engine(test_config):
#     return create_async_engine(test_config.database_url, poolclass=NullPool)


@pytest.fixture(scope="session")
def sessionmaker(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
async def session(engine, sessionmaker) -> AsyncSession:
    async with engine.connect() as connection:
        trans = await connection.begin()

        async with sessionmaker(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
            autoflush=False,
        ) as async_session:
            yield async_session

        await trans.rollback()


# @pytest.fixture
# @pytest.mark.asyncio
# async def get_async_session_mock(session, mocker):
#     session_mock = mocker.AsyncMock()
#     session_mock.__aiter__.return_value = [session]
#
#     return session_mock


@pytest.fixture
async def client(session):
    app.dependency_overrides[get_async_session] = lambda: session

    async with AsyncClient(app=app, base_url="http://test.com") as async_client:
        yield async_client
