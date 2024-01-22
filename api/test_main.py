from async_asgi_testclient import TestClient
import pytest

from .main import app


@pytest.fixture
async def client():
    async with TestClient(app) as client:
        yield client

@pytest.mark.asyncio
async def test_create_post(client: TestClient):
    response = await client.get("/")
    assert response.status_code == 201
