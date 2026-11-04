import asyncio
import time

from nicegui import core
from nicegui.app.app import prune_tab_storage
from nicegui.client import Client
from nicegui.observables import ObservableDict


class _DummyClient:
    """Minimal stand-in for a connected client holding on to a tab storage."""

    def __init__(self, tab_id: str) -> None:
        self.tab_id = tab_id
        self._pinned_tab_id = tab_id


def _ancient_tab() -> ObservableDict:
    tab = ObservableDict({'key': 'value'})
    tab.last_modified = 0.0  # older than any max_tab_storage_age
    return tab


def _prune(**kwargs) -> None:
    # Do not use asyncio.run: it resets the policy's current event loop to ``None``,
    # which orphans a loop installed by an earlier test and turns it into an
    # "unclosed event loop" ResourceWarning once the next test collects garbage.
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(prune_tab_storage(**kwargs))
    finally:
        loop.close()


def test_prune_tab_storage_removes_stale_orphan_tab():
    storage = core.app.storage
    storage._tabs['orphan'] = _ancient_tab()  # pylint: disable=protected-access
    try:
        _prune()
        assert 'orphan' not in storage._tabs  # pylint: disable=protected-access
    finally:
        storage._tabs.clear()  # pylint: disable=protected-access


def test_prune_tab_storage_keeps_tab_of_connected_client():
    storage = core.app.storage
    storage._tabs['active'] = _ancient_tab()  # pylint: disable=protected-access
    storage._tabs['orphan'] = _ancient_tab()  # pylint: disable=protected-access
    Client.instances['dummy'] = _DummyClient('active')  # type: ignore[assignment]
    try:
        _prune()
        tabs = storage._tabs  # pylint: disable=protected-access
        assert storage._tabs['active'] == {'key': 'value'}  # data is not cleared
        assert 'orphan' not in tabs
    finally:
        del Client.instances['dummy']
        storage._tabs.clear()  # pylint: disable=protected-access


def test_prune_tab_storage_force_still_prunes_active_tab():
    storage = core.app.storage
    storage._tabs['active'] = _ancient_tab()  # pylint: disable=protected-access
    Client.instances['dummy'] = _DummyClient('active')  # type: ignore[assignment]
    try:
        _prune(force=True)
        assert 'active' not in storage._tabs  # pylint: disable=protected-access
    finally:
        del Client.instances['dummy']
        storage._tabs.clear()  # pylint: disable=protected-access


def test_prune_tab_storage_keeps_recent_orphan_tab():
    storage = core.app.storage
    recent = ObservableDict({'key': 'value'})
    recent.last_modified = time.time()
    storage._tabs['recent'] = recent  # pylint: disable=protected-access
    try:
        _prune()
        assert storage._tabs['recent'] == {'key': 'value'}  # pylint: disable=protected-access
    finally:
        storage._tabs.clear()  # pylint: disable=protected-access
