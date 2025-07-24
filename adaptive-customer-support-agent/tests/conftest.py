"""
Global test fixtures and mocks.
"""
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
