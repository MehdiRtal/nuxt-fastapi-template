from async_asgi_testclient import TestClient
import pytest_asyncio

from src.main import app

@pytest_asyncio.fixture
async def client():
    async with TestClient(app) as client:
        yield client
