from async_asgi_testclient import TestClient
import pytest_asyncio
import os
from pytest_asyncio import is_async_test
import pytest

from src.main import app


os.environ["ENVIRONEMENT"] = "TEST"

def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)

@pytest_asyncio.fixture(scope="session")
async def client():
    async with TestClient(app, headers={"X-Forwarded-For": "123.123.123.123"}) as client:
        yield client
