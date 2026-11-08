from unittest.mock import AsyncMock, MagicMock

import pytest

from nicegui.persistence.redis_persistent_dict import RedisPersistentDict

pytest.importorskip('redis')


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


@pytest.mark.asyncio
async def test_prune_tab_storage_refreshes_ttl_of_pinned_tabs(monkeypatch):
    """The prune tick must refresh the Redis TTL of tab storages pinned to a
    connected client (issue #6487) - the regression that direct refresh_ttl
    tests cannot catch."""
    from nicegui import core
    from nicegui.app import app as app_module

    d = RedisPersistentDict.__new__(RedisPersistentDict)
    d.key = 'nicegui:tab-pinned'
    d.ttl = 3600
    d.last_modified = 0.0  # long expired, but pinned
    d.redis_client = MagicMock()
    d.redis_client.expire = AsyncMock()
    d.clear = MagicMock()
    d.close = AsyncMock()

    class FakeClient:
        _pinned_tab_id = 'tab-pinned'

    class FakeInstances:
        def values(self):
            return [FakeClient()]

    # core.app.storage._tabs holds the pinned, long-expired tab storage.
    monkeypatch.setattr(core.app.storage, '_tabs', {'tab-pinned': d})
    monkeypatch.setattr(core.app.storage, 'max_tab_storage_age', 3600)
    monkeypatch.setattr(app_module.Client, 'instances', FakeInstances())

    await app_module.prune_tab_storage()

    d.redis_client.expire.assert_awaited_once_with('nicegui:tab-pinned', 3600)
    d.clear.assert_not_called()
    d.close.assert_not_awaited()
