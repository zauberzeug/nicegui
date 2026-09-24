import asyncio
from collections.abc import Callable

import pytest

from nicegui import background_tasks, ui
from nicegui.testing import User


@pytest.mark.parametrize('create_element', [
    ui.leaflet,
    ui.scene,
    lambda: ui.scene_view(ui.scene()),
], ids=['leaflet', 'scene', 'scene_view'])
async def test_initialized_is_cancelled_when_client_is_deleted(user: User, create_element: Callable[[], ui.leaflet | ui.scene | ui.scene_view]):
    """The task awaiting an element's initialization must be cancelled when the client is deleted, e.g. after a disconnect."""
    results = []

    @ui.page('/')
    async def page():
        element = create_element()
        await element.initialized()
        results.append('initialized')  # must not run: the client is gone before the element can initialize

    client = await user.open('/')
    await asyncio.sleep(0.1)  # let the page function start awaiting the initialization
    client.delete()
    await asyncio.sleep(0.1)  # let the cancellation take effect
    assert not results, 'code after initialized() must not run when the client is deleted'
    assert not any('wait for result of page' in task.get_name() for task in background_tasks.running_tasks), \
        'the awaiting task should be cancelled, not leaked'


async def test_initialized_resolves_after_init_even_when_client_is_disconnected(user: User):
    """Once an element is initialized, awaiting it must resolve right away instead of waiting for a reconnect."""
    results = []

    @ui.page('/')
    def page():
        scene = ui.scene()

        async def wait_for_init() -> None:
            await scene.initialized()
            results.append('initialized')

        ui.button('Wait', on_click=wait_for_init)

    client = await user.open('/')
    user.find(ui.scene).trigger('init')
    client.tab_id = None  # simulate a browser disconnect
    user.find('Wait').click()
    await asyncio.sleep(0.1)
    assert results == ['initialized'], 'initialized() should resolve immediately for an already initialized element'
