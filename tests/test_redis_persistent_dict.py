import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

pytest.importorskip('redis')

from nicegui.persistence.redis_persistent_dict import RedisPersistentDict


@pytest.fixture
def dict_with_ttl() -> RedisPersistentDict:
    d = RedisPersistentDict.__new__(RedisPersistentDict)
    d.key = 'nicegui:tab-test'
    d.ttl = 3600
    d.redis_client = MagicMock()
    d.redis_client.expire = AsyncMock()
    return d


@pytest.mark.asyncio
async def test_refresh_ttl_renews_the_key_expiry(dict_with_ttl: RedisPersistentDict):
    await dict_with_ttl.refresh_ttl()
    dict_with_ttl.redis_client.expire.assert_awaited_once_with('nicegui:tab-test', 3600)


@pytest.mark.asyncio
async def test_refresh_ttl_is_a_noop_without_ttl():
    d = RedisPersistentDict.__new__(RedisPersistentDict)
    d.key = 'nicegui:user-test'
    d.ttl = None
    d.redis_client = MagicMock()
    d.redis_client.expire = AsyncMock()

    await d.refresh_ttl()

    d.redis_client.expire.assert_not_awaited()
