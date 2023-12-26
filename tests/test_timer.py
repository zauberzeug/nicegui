import asyncio

import pytest

from nicegui import ui

from .screen import Screen


class Counter:
    value = 0

    def increment(self):
        self.value += 1


def test_timer(screen: Screen):
    counter = Counter()
    t = ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    screen.wait(0.5)
    assert counter.value == 0, 'timer is not running'

    screen.start_server()
    screen.wait(0.5)
    assert counter.value > 0, 'timer is running after starting the server'

    t.deactivate()
    screen.wait(0.5)
    c = counter.value
    screen.wait(0.5)
    assert counter.value == c, 'timer is not running anymore after deactivating it'

    t.activate()
    screen.wait(0.5)
    assert counter.value > c, 'timer is running again after activating it'

    t.cancel()
    screen.wait(0.5)
    c = counter.value
    screen.wait(0.5)
    assert counter.value == c, 'timer is not running anymore after canceling it'


def test_timer_on_private_page(screen: Screen):
    counter = Counter()

    @ui.page('/', reconnect_timeout=0)
    def page():
        ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    screen.start_server()
    screen.wait(0.5)
    assert counter.value == 0, 'timer is not running even after starting the server'

    screen.open('/')
    screen.wait(0.5)
    assert counter.value > 0, 'timer is running after opening the page'

    screen.close()
    count = counter.value
    screen.wait(0.5)
    assert counter.value == count, 'timer is not running anymore after closing the page'


@pytest.mark.parametrize('once', [True, False])
def test_setting_visibility(screen: Screen, once: bool):
    """reproduction of https://github.com/zauberzeug/nicegui/issues/206"""
    @ui.page('/')
    def page():
        label = ui.label('Some Label')
        ui.timer(0.1, lambda: label.set_visibility(False), once=once)

    screen.open('/')
    screen.wait(0.5)
    screen.should_not_contain('Some Label')


def test_awaiting_coroutine(screen: Screen):
    user = {'name': 'John Doe'}

    async def update_user():
        await asyncio.sleep(0.1)
        user['name'] = 'Jane Doe'

    ui.timer(1, update_user)

    screen.open('/')
    screen.wait(1)
    assert user['name'] == 'Jane Doe'


def test_timer_on_deleted_container(screen: Screen):
    state = {'count': 0}
    with ui.row() as outer_container:
        with ui.row():
            ui.timer(0.1, lambda: state.update(count=state['count'] + 1))

    ui.button('delete', on_click=outer_container.clear)

    screen.open('/')
    screen.click('delete')
    screen.wait(0.5)
    count = state['count']
    screen.wait(0.5)
    assert state['count'] == count, 'timer is not running anymore after deleting the container'
