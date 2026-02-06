import asyncio
import gc

import httpx
import pytest

from nicegui import Client, app, ui
from nicegui.testing import SharedScreen, User


class Counter:
    value = 0

    def increment(self):
        self.value += 1


def test_timer(shared_screen: SharedScreen):
    counter = Counter()
    t = None

    @ui.page('/')
    def page():
        nonlocal t
        t = ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    shared_screen.wait(0.5)
    assert counter.value == 0, 'timer is not running'

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert counter.value > 0, 'timer is running after opening the page'

    t.deactivate()
    shared_screen.wait(0.5)
    c = counter.value
    shared_screen.wait(0.5)
    assert counter.value == c, 'timer is not running anymore after deactivating it'

    t.activate()
    shared_screen.wait(0.5)
    assert counter.value > c, 'timer is running again after activating it'

    t.cancel()
    shared_screen.wait(0.5)
    c = counter.value
    shared_screen.wait(0.5)
    assert counter.value == c, 'timer is not running anymore after canceling it'


def test_timer_on_private_page(shared_screen: SharedScreen):
    counter = Counter()

    @ui.page('/', reconnect_timeout=0)
    def page():
        ui.timer(0.1, counter.increment)

    assert counter.value == 0, 'count is initially zero'
    shared_screen.start_server()
    shared_screen.wait(0.5)
    assert counter.value == 0, 'timer is not running even after starting the server'

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert counter.value > 0, 'timer is running after opening the page'

    shared_screen.close()
    count = counter.value
    shared_screen.wait(0.5)
    assert counter.value == count, 'timer is not running anymore after closing the page'


@pytest.mark.parametrize('once', [True, False])
def test_setting_visibility(shared_screen: SharedScreen, once: bool):
    """reproduction of https://github.com/zauberzeug/nicegui/issues/206"""
    @ui.page('/')
    def page():
        label = ui.label('Some Label')
        ui.timer(0.1, lambda: label.set_visibility(False), once=once)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Some Label')


def test_awaiting_coroutine(shared_screen: SharedScreen):
    user = {'name': 'Alice'}

    async def update_user():
        await asyncio.sleep(0.1)
        user['name'] = 'Bob'

    @ui.page('/')
    def page():
        ui.timer(0.5, update_user)

    shared_screen.open('/')
    shared_screen.wait(1)
    assert user['name'] == 'Bob'


def test_timer_on_deleted_container(shared_screen: SharedScreen):
    state = {'count': 0}

    @ui.page('/')
    def page():
        with ui.row() as outer_container:
            with ui.row():
                ui.timer(0.1, lambda: state.update(count=state['count'] + 1))

        ui.button('delete', on_click=outer_container.clear)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.click('delete')
    shared_screen.wait(0.5)
    count = state['count']
    shared_screen.wait(0.5)
    assert state['count'] == count, 'timer is not running anymore after deleting the container'


def test_different_callbacks(shared_screen: SharedScreen):
    def sync_function():
        ui.label('a synchronous function')

    async def async_function():
        await asyncio.sleep(0.1)
        ui.label('an asynchronous function')

    async def async_lambda(msg: str):
        await asyncio.sleep(0.1)
        ui.label(f'an asynchronous lambda: {msg}')

    @ui.page('/')
    def page():
        ui.timer(0.1, sync_function, once=True)
        ui.timer(0.1, async_function, once=True)
        ui.timer(0.1, lambda: ui.label('a synchronous lambda'), once=True)
        ui.timer(0.1, lambda: async_lambda('Hi!'), once=True)

    shared_screen.open('/')
    shared_screen.should_contain('a synchronous function')
    shared_screen.should_contain('an asynchronous function')
    shared_screen.should_contain('a synchronous lambda')
    shared_screen.should_contain('an asynchronous lambda: Hi!')


async def test_cleanup(user: User):
    @ui.page('/')
    def page():
        def update():
            ui.timer(0.01, update, once=True)
        ui.timer(0, update, once=True)

    def count():
        return sum(1 for obj in gc.get_objects() if isinstance(obj, ui.timer))

    await user.open('/')
    assert count() > 0, 'there are timer objects in memory'
    await asyncio.sleep(0.1)
    gc.collect()
    assert count() == 1, 'only current timer object is in memory'


def test_app_timer(shared_screen: SharedScreen):
    counter = Counter()
    timer = app.timer(0.1, counter.increment)

    @ui.page('/')
    def page():
        ui.button('Activate', on_click=timer.activate)
        ui.button('Deactivate', on_click=timer.deactivate)

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert counter.value > 0, 'timer is running after starting the server'

    shared_screen.click('Deactivate')
    value = counter.value
    shared_screen.wait(0.5)
    assert counter.value == value, 'timer is not running anymore after deactivating it'

    shared_screen.click('Activate')
    shared_screen.wait(0.5)
    assert counter.value > value, 'timer is running again after activating it'
    value = counter.value

    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert counter.value > value, 'timer is also incrementing when opening another page'


def test_cancel_current_invocation(shared_screen: SharedScreen):
    counter = Counter()

    async def update():
        await asyncio.sleep(1.0)
        counter.increment()

    @ui.page('/')
    def page():
        t = ui.timer(0, update, once=True)
        ui.button('Cancel with current invocation', on_click=lambda: t.cancel(with_current_invocation=True))

    shared_screen.open('/')
    shared_screen.wait(0.2)

    shared_screen.click('Cancel with current invocation')
    shared_screen.wait(1.2)
    assert counter.value == 0


def test_cancel_before_invocation_starts(shared_screen: SharedScreen):
    counter = Counter()

    async def update():
        await asyncio.sleep(0.2)
        counter.increment()

    @ui.page('/')
    def page():
        # use a small delay before first invocation to ensure we cancel before it starts
        t = ui.timer(0.5, update, once=True)
        ui.button('Cancel with current invocation', on_click=lambda: t.cancel(with_current_invocation=True))

    shared_screen.open('/')
    shared_screen.wait(0.1)

    shared_screen.click('Cancel with current invocation')
    shared_screen.wait(0.6)
    assert counter.value == 0


def test_error_in_callback(shared_screen: SharedScreen):
    @ui.page('/')
    def index():
        ui.timer(0, lambda: print(1 / 0), once=True)

    app.on_exception(lambda e: ui.notification(f'Exception: {e}'))

    shared_screen.open('/')
    shared_screen.should_contain('Exception: division by zero')
    shared_screen.assert_py_logger('ERROR', 'division by zero')


def test_no_leak_when_client_deleted(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.timer(0.1, lambda: None)

    shared_screen.start_server()
    httpx.get(shared_screen.url)
    shared_screen.wait(1)
    Client.prune_instances(client_age_threshold=0)
    shared_screen.wait(1)
    assert not any(isinstance(obj, ui.timer) for obj in gc.get_objects())
