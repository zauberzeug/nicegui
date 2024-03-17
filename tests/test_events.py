import asyncio
from typing import Literal

import pytest
from selenium.webdriver.common.by import By

from nicegui import ui
from nicegui.events import ClickEventArguments
from nicegui.testing import Screen


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


def test_click_events(screen: Screen):
    ui.button('click_sync_no_args', on_click=click_sync_no_args)
    ui.button('click_sync_with_args', on_click=click_sync_with_args)
    ui.button('click_async_no_args', on_click=click_async_no_args)
    ui.button('click_async_with_args', on_click=click_async_with_args)
    ui.button('click_lambda_with_async_and_parameters', on_click=lambda: click_lambda_with_async_and_parameters('works'))

    screen.open('/')
    screen.click('click_sync_no_args')
    screen.click('click_sync_with_args')
    screen.click('click_async_no_args')
    screen.click('click_async_with_args')
    screen.click('click_lambda_with_async_and_parameters')
    screen.should_contain('click_sync_no_args')
    screen.should_contain('click_sync_with_args')
    screen.should_contain('click_async_no_args')
    screen.should_contain('click_async_with_args')
    screen.should_contain('click_lambda_with_async_and_parameters: works')


def test_generic_events(screen: Screen):
    ui.label('click_sync_no_args').on('click', click_sync_no_args, [])
    ui.label('click_sync_with_args').on('click', click_sync_with_args, [])
    ui.label('click_async_no_args').on('click', click_async_no_args, [])
    ui.label('click_async_with_args').on('click', click_async_with_args, [])

    screen.open('/')
    screen.click('click_sync_no_args')
    screen.click('click_sync_with_args')
    screen.click('click_async_no_args')
    screen.click('click_async_with_args')
    screen.should_contain('click_sync_no_args')
    screen.should_contain('click_sync_with_args')
    screen.should_contain('click_async_no_args')
    screen.should_contain('click_async_with_args')


def test_event_with_update_before_await(screen: Screen):
    @ui.page('/')
    def page():
        async def update():
            ui.label('1')
            await asyncio.sleep(1.0)
            ui.label('2')

        ui.button('update', on_click=update)

    screen.open('/')
    screen.click('update')
    screen.should_contain('1')
    screen.should_not_contain('2')
    screen.should_contain('2')


def test_event_modifiers(screen: Screen):
    events = []
    ui.input('A').on('keydown', lambda _: events.append('A'), [])
    ui.input('B').on('keydown.x', lambda _: events.append('B'), [])
    ui.input('C').on('keydown.once', lambda _: events.append('C'), [])
    ui.input('D').on('keydown.shift.x', lambda _: events.append('D'), [])

    screen.open('/')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="A"]').send_keys('x')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="B"]').send_keys('xy')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="C"]').send_keys('xx')
    screen.selenium.find_element(By.XPATH, '//*[@aria-label="D"]').send_keys('Xx')
    assert events == ['A', 'B', 'C', 'D']


def test_throttling(screen: Screen):
    events = []
    ui.button('Test', on_click=lambda: events.append(1)).on('click', lambda: events.append(2), [], throttle=1)

    screen.open('/')
    screen.click('Test')
    screen.click('Test')
    screen.click('Test')
    assert events == [1, 2, 1, 1]

    screen.wait(1.1)
    assert events == [1, 2, 1, 1, 2]

    screen.click('Test')
    screen.click('Test')
    screen.click('Test')
    assert events == [1, 2, 1, 1, 2, 1, 2, 1, 1]


def test_throttling_variants(screen: Screen):
    events = []
    value = 0
    ui.button('Both').on('click', lambda: events.append(value), [], throttle=1)
    ui.button('Leading').on('click', lambda: events.append(value), [], throttle=1, trailing_events=False)
    ui.button('Trailing').on('click', lambda: events.append(value), [], throttle=1, leading_events=False)

    screen.open('/')
    value = 1
    screen.click('Both')
    value = 2
    screen.click('Both')
    value = 3
    screen.click('Both')
    assert events == [1]
    screen.wait(1.1)
    assert events == [1, 3]

    events = []
    value = 1
    screen.click('Leading')
    value = 2
    screen.click('Leading')
    value = 3
    screen.click('Leading')
    assert events == [1]
    screen.wait(1.1)
    assert events == [1]

    events = []
    value = 1
    screen.click('Trailing')
    value = 2
    screen.click('Trailing')
    value = 3
    screen.click('Trailing')
    assert events == []  # pylint: disable=use-implicit-booleaness-not-comparison
    screen.wait(1.1)
    assert events == [3]


@pytest.mark.parametrize('attribute', ['disabled', 'hidden'])
def test_server_side_validation(screen: Screen, attribute: Literal['disabled', 'hidden']):
    b = ui.button('Button', on_click=lambda: ui.label('Success'))
    if attribute == 'disabled':
        b.disable()
    else:
        b.set_visibility(False)
    ui.button('Hack', on_click=lambda: ui.run_javascript(f'''
        getElement({b.id}).$emit("click", {{"id": {b.id}, "listener_id": "{list(b._event_listeners.keys())[0]}"}});
    '''))  # pylint: disable=protected-access

    screen.open('/')
    screen.click('Hack')
    screen.wait(0.5)
    screen.should_not_contain('Success')


def test_js_handler(screen: Screen) -> None:
    ui.button('Button').on('click', js_handler='() => document.body.appendChild(document.createTextNode("Click!"))')

    screen.open('/')
    screen.click('Button')
    screen.should_contain('Click!')
