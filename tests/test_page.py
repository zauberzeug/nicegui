import asyncio
import re
from typing import Literal

import pytest
from fastapi.responses import PlainTextResponse
from selenium.webdriver.common.by import By

from nicegui import app, background_tasks, ui
from nicegui.testing import Screen, SharedScreen


def test_page(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    shared_screen.should_contain('NiceGUI')
    shared_screen.should_contain('Hello, world!')


def test_custom_title(shared_screen: SharedScreen):
    @ui.page('/', title='My Custom Title')
    def page():
        ui.label('Hello, world!')

    shared_screen.open('/')
    shared_screen.should_contain('My Custom Title')
    shared_screen.should_contain('Hello, world!')


def test_route_with_custom_path(shared_screen: SharedScreen):
    @ui.page('/test_route')
    def page():
        ui.label('page with custom path')

    shared_screen.open('/test_route')
    shared_screen.should_contain('page with custom path')


def test_link_to_page_by_passing_function(shared_screen: SharedScreen):
    @ui.page('/subpage')
    def subpage():
        ui.label('the subpage')

    @ui.page('/')
    def page():
        ui.link('link to subpage', subpage)

    shared_screen.open('/')
    shared_screen.click('link to subpage')
    shared_screen.should_contain('the subpage')


def test_creating_new_page_after_startup(shared_screen: SharedScreen):
    shared_screen.start_server()

    @ui.page('/late_page')
    def page():
        ui.label('page created after startup')

    shared_screen.open('/late_page')
    shared_screen.should_contain('page created after startup')


def test_wait_for_connected(shared_screen: SharedScreen):
    label: ui.label | None = None

    async def load() -> None:
        assert label
        label.text = 'loading...'
        # NOTE we can not use asyncio.create_task() here because we are on a different thread than the NiceGUI event loop
        background_tasks.create(takes_a_while())

    async def takes_a_while() -> None:
        await asyncio.sleep(0.1)
        assert label
        label.text = 'delayed data has been loaded'

    @ui.page('/')
    async def page():
        nonlocal label
        label = ui.label()
        await ui.context.client.connected()
        await load()

    shared_screen.open('/')
    shared_screen.should_contain('delayed data has been loaded')


def test_wait_for_disconnect(shared_screen: SharedScreen):
    events = []

    @ui.page('/', reconnect_timeout=0)
    async def page():
        await ui.context.client.connected()
        events.append('connected')
        await ui.context.client.disconnected()
        events.append('disconnected')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert events == ['connected', 'disconnected', 'connected']


def test_wait_for_disconnect_without_awaiting_connected(shared_screen: SharedScreen):
    events = []

    @ui.page('/', reconnect_timeout=0)
    async def page():
        await ui.context.client.disconnected()
        events.append('disconnected')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.open('/')
    shared_screen.wait(0.5)
    assert events == ['disconnected']


def test_adding_elements_after_connected(shared_screen: SharedScreen):
    @ui.page('/')
    async def page():
        ui.label('before')
        await ui.context.client.connected()
        ui.label('after')

    shared_screen.open('/')
    shared_screen.should_contain('before')
    shared_screen.should_contain('after')


def test_exception(shared_screen: SharedScreen):
    exceptions = []

    @ui.page('/')
    def page():
        ui.on_exception(exceptions.append)
        raise RuntimeError('some exception')

    shared_screen.allowed_js_errors.append('/ - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('500')
    shared_screen.should_contain('Server error')
    shared_screen.assert_py_logger('ERROR', 'some exception')
    assert not exceptions, 'ui.on_exception is for in-page exceptions (after page sent to browser)'


def test_exception_after_connected(shared_screen: SharedScreen):
    exceptions = []

    @ui.page('/')
    async def page():
        ui.on_exception(exceptions.append)
        await ui.context.client.connected()
        ui.label('this is shown')
        raise RuntimeError('some exception')

    shared_screen.open('/')
    shared_screen.should_contain('this is shown')
    shared_screen.assert_py_logger('ERROR', 'some exception')
    assert exceptions, 'in-page exception should be caught by ui.on_exception'


def test_api_exception(shared_screen: SharedScreen):
    @app.get('/')
    def api_exception():
        raise RuntimeError('some exception in a GET endpoint')

    shared_screen.allowed_js_errors.append('/ - Failed to load resource')
    shared_screen.allowed_js_errors.append('/favicon.ico - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('Internal Server Error')


def test_page_with_args(shared_screen: SharedScreen):
    @ui.page('/page/{id_}')
    def page(id_: int):
        ui.label(f'Page {id_}')

    shared_screen.open('/page/42')
    shared_screen.should_contain('Page 42')


def test_adding_elements_during_onconnect(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Label 1')
        ui.context.client.on_connect(lambda: ui.label('Label 2'))

    shared_screen.open('/')
    shared_screen.should_contain('Label 2')


def test_async_connect_handler(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def run_js():
            result.text = await ui.run_javascript('41 + 1')
        result = ui.label()
        ui.context.client.on_connect(run_js)

    shared_screen.open('/')
    shared_screen.should_contain('42')


@pytest.mark.parametrize('unocss', [None, 'mini', 'wind3', 'wind4'])
def test_dark_mode(screen: Screen, unocss: Literal['mini', 'wind3', 'wind4'] | None):
    app.config.unocss = unocss

    @ui.page('/auto', dark=None)
    def page():
        ui.label('A').classes('text-blue-400 dark:text-red-400')

    @ui.page('/light', dark=False)
    def light_page():
        ui.label('B').classes('text-blue-400 dark:text-red-400')

    @ui.page('/dark', dark=True)
    def dark_page():
        ui.label('C').classes('text-blue-400 dark:text-red-400')

    blue = 'oklch(0.707 0.165 254.624)'
    red = 'oklch(0.704 0.191 22.216)'
    white = 'rgba(0, 0, 0, 0)'
    black = 'rgba(18, 18, 18, 1)'

    screen.open('/auto')
    assert screen.find('A').value_of_css_property('color') == blue
    assert screen.find_by_tag('body').value_of_css_property('background-color') == white

    screen.open('/light')
    assert screen.find('B').value_of_css_property('color') == blue
    assert screen.find_by_tag('body').value_of_css_property('background-color') == white

    screen.open('/dark')
    assert screen.find('C').value_of_css_property('color') == red
    assert screen.find_by_tag('body').value_of_css_property('background-color') == black


def test_returning_custom_response(shared_screen: SharedScreen):
    @ui.page('/')
    def page(plain: bool = False):
        if plain:
            return PlainTextResponse('custom response')
        else:
            ui.label('normal NiceGUI page')

    shared_screen.allowed_js_errors.append('/favicon.ico - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('normal NiceGUI page')
    shared_screen.should_not_contain('custom response')
    shared_screen.open('/?plain=true')
    shared_screen.should_contain('custom response')
    shared_screen.should_not_contain('normal NiceGUI page')


def test_returning_custom_response_async(shared_screen: SharedScreen):
    @ui.page('/')
    async def page(plain: bool = False):
        await asyncio.sleep(0.01)  # simulates a db request or similar
        if plain:
            return PlainTextResponse('custom response')
        else:
            ui.label('normal NiceGUI page')

    shared_screen.allowed_js_errors.append('/favicon.ico - Failed to load resource')
    shared_screen.open('/')
    shared_screen.should_contain('normal NiceGUI page')
    shared_screen.should_not_contain('custom response')
    shared_screen.open('/?plain=true')
    shared_screen.should_contain('custom response')
    shared_screen.should_not_contain('normal NiceGUI page')


def test_warning_about_to_late_responses(shared_screen: SharedScreen):
    @ui.page('/')
    async def page():
        await ui.context.client.connected()
        ui.label('NiceGUI page')
        return PlainTextResponse('custom response')

    shared_screen.open('/')
    shared_screen.should_contain('NiceGUI page')
    shared_screen.assert_py_logger('ERROR', re.compile('it was returned after the HTML had been delivered to the client'))


def test_reconnecting_without_page_reload(shared_screen: SharedScreen):
    @ui.page('/', reconnect_timeout=3.0)
    def page():
        ui.input('Input').props('autofocus')
        ui.button('drop connection', on_click=lambda: ui.run_javascript('socket.io.engine.close()'))

    shared_screen.open('/')
    shared_screen.type('hello')
    shared_screen.click('drop connection')
    shared_screen.wait(2.0)
    element = shared_screen.selenium.find_element(By.XPATH, '//*[@aria-label="Input"]')
    assert element.get_attribute('value') == 'hello', 'input should be preserved after reconnect (i.e. no page reload)'


def test_ip(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label(ui.context.client.ip or 'unknown')

    shared_screen.open('/')
    shared_screen.should_contain('127.0.0.1')


def test_multicast(shared_screen: SharedScreen):
    def update():
        for client in app.clients('/'):
            with client:
                ui.label('added')

    @ui.page('/')
    def page():
        ui.button('add label', on_click=update)

    shared_screen.open('/')
    shared_screen.switch_to(1)
    shared_screen.open('/')
    shared_screen.click('add label')
    shared_screen.should_contain('added')
    shared_screen.switch_to(0)
    shared_screen.should_contain('added')


def test_warning_if_response_takes_too_long(shared_screen: SharedScreen):
    @ui.page('/', response_timeout=0.5)
    async def page():
        await asyncio.sleep(1)
        ui.label('all done')

    shared_screen.allowed_js_errors.append('/ - Failed to load resource')
    shared_screen.open('/')
    shared_screen.assert_py_logger('WARNING', re.compile('Response for / not ready after 0.5 seconds'))
