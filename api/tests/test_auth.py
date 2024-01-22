from async_asgi_testclient import TestClient
from fastapi import status
import pytest


@pytest.mark.asyncio
async def test_login(client: TestClient):
    body = {
        "username": "admin",
        "password": "admin"
    }
    response = await client.post("/auth/login", form=body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
