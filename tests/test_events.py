import asyncio
from typing import Literal

import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.events import ClickEventArguments
from nicegui.testing import SharedScreen


def click_sync_no_args():
    ui.label('click_sync_no_args')


def click_sync_with_args(_: ClickEventArguments):
    ui.label('click_sync_with_args')


async def click_async_no_args():
    await asyncio.sleep(0.1)
    ui.label('click_async_no_args')


async def click_async_with_args(_: ClickEventArguments):
    await asyncio.sleep(0.1)
    ui.label('click_async_with_args')


async def click_lambda_with_async_and_parameters(msg: str):
    await asyncio.sleep(0.1)
    ui.label(f'click_lambda_with_async_and_parameters: {msg}')


def test_click_events(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('click_sync_no_args', on_click=click_sync_no_args)
        ui.button('click_sync_with_args', on_click=click_sync_with_args)
        ui.button('click_async_no_args', on_click=click_async_no_args)
        ui.button('click_async_with_args', on_click=click_async_with_args)
        ui.button('click_lambda_with_async_and_parameters',
                  on_click=lambda: click_lambda_with_async_and_parameters('works'))

    shared_screen.open('/')
    shared_screen.click('click_sync_no_args')
    shared_screen.click('click_sync_with_args')
    shared_screen.click('click_async_no_args')
    shared_screen.click('click_async_with_args')
    shared_screen.click('click_lambda_with_async_and_parameters')
    shared_screen.should_contain('click_sync_no_args')
    shared_screen.should_contain('click_sync_with_args')
    shared_screen.should_contain('click_async_no_args')
    shared_screen.should_contain('click_async_with_args')
    shared_screen.should_contain('click_lambda_with_async_and_parameters: works')


def test_generic_events(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('click_sync_no_args').on('click', click_sync_no_args, [])
        ui.label('click_sync_with_args').on('click', click_sync_with_args, [])
        ui.label('click_async_no_args').on('click', click_async_no_args, [])
        ui.label('click_async_with_args').on('click', click_async_with_args, [])

    shared_screen.open('/')
    shared_screen.click('click_sync_no_args')
    shared_screen.click('click_sync_with_args')
    shared_screen.click('click_async_no_args')
    shared_screen.click('click_async_with_args')
    shared_screen.should_contain('click_sync_no_args')
    shared_screen.should_contain('click_sync_with_args')
    shared_screen.should_contain('click_async_no_args')
    shared_screen.should_contain('click_async_with_args')


def test_event_with_update_before_await(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def update():
            ui.label('1')
            await asyncio.sleep(1.0)
            ui.label('2')

        ui.button('update', on_click=update)

    shared_screen.open('/')
    shared_screen.click('update')
    shared_screen.should_contain('1')
    shared_screen.should_not_contain('2')
    shared_screen.should_contain('2')


def test_event_modifiers(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    def page():
        ui.input('A').on('keydown', lambda _: events.append('A'), [])
        ui.input('B').on('keydown.x', lambda _: events.append('B'), [])
        ui.input('C').on('keydown.once', lambda _: events.append('C'), [])
        ui.input('D').on('keydown.shift.x', lambda _: events.append('D'), [])

    shared_screen.open('/')
    shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="A"]').send_keys('x')
    shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="B"]').send_keys('xy')
    shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="C"]').send_keys('xx')
    shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="D"]').send_keys('Xx')
    assert events == ['A', 'B', 'C', 'D']


def test_throttling(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    def page():
        ui.button('Test', on_click=lambda: events.append(1)).on('click', lambda: events.append(2), [], throttle=1)

    shared_screen.open('/')
    shared_screen.click('Test')
    shared_screen.click('Test')
    shared_screen.click('Test')
    assert events == [1, 2, 1, 1]

    shared_screen.wait(1.1)
    assert events == [1, 2, 1, 1, 2]

    shared_screen.click('Test')
    shared_screen.click('Test')
    shared_screen.click('Test')
    assert events == [1, 2, 1, 1, 2, 1, 2, 1, 1]


def test_throttling_variants(shared_screen: SharedScreen):
    events = []
    value = 0

    @ui.page('/')
    def page():
        ui.button('Both').on('click', lambda: events.append(value), [], throttle=1)
        ui.button('Leading').on('click', lambda: events.append(value), [], throttle=1, trailing_events=False)
        ui.button('Trailing').on('click', lambda: events.append(value), [], throttle=1, leading_events=False)

    shared_screen.open('/')
    value = 1
    shared_screen.click('Both')
    value = 2
    shared_screen.click('Both')
    value = 3
    shared_screen.click('Both')
    assert events == [1]
    shared_screen.wait(1.1)
    assert events == [1, 3]

    events = []
    value = 1
    shared_screen.click('Leading')
    value = 2
    shared_screen.click('Leading')
    value = 3
    shared_screen.click('Leading')
    assert events == [1]
    shared_screen.wait(1.1)
    assert events == [1]

    events = []
    value = 1
    shared_screen.click('Trailing')
    value = 2
    shared_screen.click('Trailing')
    value = 3
    shared_screen.click('Trailing')
    assert events == []  # pylint: disable=use-implicit-booleaness-not-comparison
    shared_screen.wait(1.1)
    assert events == [3]


@pytest.mark.parametrize('attribute', ['disabled', 'hidden'])
def test_server_side_validation(shared_screen: SharedScreen, attribute: Literal['disabled', 'hidden']):
    @ui.page('/')
    def page():
        b = ui.button('Button', on_click=lambda: ui.label('Button clicked'))
        n = ui.number('Number', on_change=lambda: ui.label('Number changed'))
        if attribute == 'disabled':
            b.disable()
            n.disable()
        else:
            b.set_visibility(False)
            n.set_visibility(False)
        ui.button('Forbidden', on_click=lambda: ui.run_javascript(f'''
            getElement({b.id}).$emit("click", {{"id": {b.id}, "listener_id": "{next(iter(b._event_listeners))}"}});
        '''))  # pylint: disable=protected-access
        ui.button('Allowed', on_click=lambda: n.set_value(42))

    shared_screen.open('/')
    shared_screen.click('Forbidden')
    shared_screen.wait(0.5)
    shared_screen.should_not_contain('Button clicked')  # triggering the click event through JavaScript does not work

    shared_screen.click('Allowed')
    shared_screen.should_contain('Number changed')  # triggering the change event through Python works


def test_js_handler(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    def page():
        ui.button('Button').on('click', js_handler='() => document.body.appendChild(document.createTextNode("Click!"))')

    shared_screen.open('/')
    shared_screen.click('Button')
    shared_screen.should_contain('Click!')


def test_delegated_event_with_argument_filtering(shared_screen: SharedScreen) -> None:
    ids = []

    @ui.page('/')
    def page():
        ui.html('''
            <p data-id="A">Item A</p>
            <p data-id="B">Item B</p>
            <p data-id="C">Item C</p>
        ''', sanitize=False).on('click', lambda e: ids.append(e.args), js_handler='(e) => emit(e.target.dataset.id)')

    shared_screen.open('/')
    shared_screen.click('Item A')
    shared_screen.click('Item B')
    shared_screen.click('Item C')
    shared_screen.wait(0.5)
    assert ids == ['A', 'B', 'C']


def test_value_change_event_arguments(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    def page():
        ui.checkbox('Checkbox', on_change=lambda e: events.append((e.value, e.previous_value)))

    shared_screen.open('/')
    shared_screen.click('Checkbox')
    shared_screen.wait(0.5)
    assert events == [(True, False)]

    shared_screen.click('Checkbox')
    shared_screen.wait(0.5)
    assert events == [(True, False), (False, True)]


async def test_late_event_registration(shared_screen: SharedScreen):
    events = []

    @ui.page('/')
    async def page():
        name = ui.input('Name')
        name.on('keydown.a', lambda: events.append('A'))
        await ui.context.client.connected()
        name.on('keydown.b', lambda: events.append('B'))
        ui.label('Ready')

    shared_screen.open('/')
    shared_screen.should_contain('Ready')
    shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Name"]').send_keys('ab')
    assert events == ['A', 'B']
    assert 'Event listeners changed after initial definition. Re-rendering affected elements.' in shared_screen.render_js_logs()
    shared_screen.assert_py_logger('WARNING',
                            'Event listeners changed after initial definition. Re-rendering affected elements.')
