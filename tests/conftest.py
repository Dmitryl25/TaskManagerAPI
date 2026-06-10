import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings
from app.db.base import Base
from app.api.deps import get_db, get_redis
from app.main import app
from app.core.limiter import limiter

from app.models.user import User  # noqa: F401
from app.models.token import Token  # noqa: F401
from app.models.workspace import WorkSpace, WorkSpaceMember  # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.task import Task  # noqa: F401
from app.models.comment import Comment  # noqa: F401
from app.models.attachment import Attachment  # noqa: F401


@pytest.fixture(autouse=True)
def mock_celery():
    with patch("app.services.user.send_welcome_email") as mock_task:
        mock_task.delay = MagicMock()
        yield


@pytest.fixture(autouse=True)
def mock_limiter(monkeypatch):
    def noop_check(request, func, in_middleware=False, *args, **kwargs):
        request.state.view_rate_limit = None

    monkeypatch.setattr(limiter, "_check_request_limit", noop_check)
    monkeypatch.setattr(limiter, "_inject_headers",
                        lambda response, view_rate_limit=None: response)


@pytest.fixture
async def setup_database():
    engine = create_async_engine(settings.test_db.database_url)

    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO admin"))

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def async_client(setup_database):
    engine = setup_database
    factory = async_sessionmaker(bind=engine, autocommit=False,
                                  autoflush=False, expire_on_commit=False)

    async def override_get_db():
        async with factory() as session:
            yield session

    async def override_get_redis():
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        yield mock_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(async_client):
    await async_client.post("/auth/register", json={"email": "user@test.com", "password": "pass1234"})
    resp = await async_client.post("/auth/login", json={"email": "user@test.com", "password": "pass1234"})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


@pytest.fixture
async def second_auth_headers(async_client):
    await async_client.post("/auth/register", json={"email": "user2@test.com", "password": "pass1234"})
    resp = await async_client.post("/auth/login", json={"email": "user2@test.com", "password": "pass1234"})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


@pytest.fixture
async def second_user_id(async_client, second_auth_headers):
    resp = await async_client.get("/users/me", headers=second_auth_headers)
    return resp.json()["id"]


@pytest.fixture
async def workspace_id(async_client, auth_headers):
    resp = await async_client.post("/workspace",
                                   json={"name": "Test Workspace", "description": "desc"},
                                   headers=auth_headers)
    return resp.json()["id"]


@pytest.fixture
async def project_id(async_client, auth_headers, workspace_id):
    resp = await async_client.post(f"/workspaces/{workspace_id}/projects",
                                   json={"name": "Test Project", "description": "desc", "key": "TP"},
                                   headers=auth_headers)
    return resp.json()["id"]


@pytest.fixture
async def task_id(async_client, auth_headers, project_id):
    resp = await async_client.post(f"/projects/{project_id}/tasks",
                                   json={"title": "Test Task"},
                                   headers=auth_headers)
    return resp.json()["id"]


@pytest.fixture
async def comment_id(async_client, auth_headers, task_id):
    resp = await async_client.post(f"/tasks/{task_id}/comments",
                                   json={"content": "Test comment"},
                                   headers=auth_headers)
    return resp.json()["id"]
