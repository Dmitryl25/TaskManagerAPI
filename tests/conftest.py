import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.api.deps import get_db
from app.main import app

import asyncio


@pytest.fixture
async def setup_database():
    engine = create_async_engine(settings.test_db.database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest.fixture
async def db_session(setup_database):
    engine = setup_database
    factory = async_sessionmaker(bind=engine, autocommit=False,
                                  autoflush=False, expire_on_commit=False)
    async with factory() as session:
        yield session


@pytest.fixture
async def async_client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()