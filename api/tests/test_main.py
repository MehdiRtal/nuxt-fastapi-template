from async_asgi_testclient import TestClient
from fastapi import status
import pytest


@pytest.mark.asyncio
async def test_root(client: TestClient):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
