from unittest.mock import patch

import aiohttp
import pytest
from fastapi.testclient import TestClient

from main import exponea_session, app

client = TestClient(app)
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
@patch('main.request', return_value=ValueError())
async def test_failed_requests(_):
    result = await exponea_session()
    assert isinstance(result, ValueError)


@pytest.mark.asyncio
async def test_timeout():
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://127.0.0.1:8000/api/smart?timeout=1')
        assert response.status == 408


@pytest.mark.asyncio
async def test_endpoint():
    async with aiohttp.ClientSession() as session:
        response = await session.get('http://127.0.0.1:8000/api/smart?timeout=100000')
        assert response.status == 200
        assert 'time' in await response.json()
