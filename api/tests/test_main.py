from async_asgi_testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_health_check(client: TestClient):
    response = await client.get("/health")
    assert response.status_code == 200
