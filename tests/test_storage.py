import asyncio
from pathlib import Path

import httpx
import pytest

from nicegui import app, background_tasks, context, ui
from nicegui import storage as storage_module
from nicegui.testing import SeleniumScreen


def test_browser_data_is_stored_in_the_browser(screen: SeleniumScreen):
    @ui.page('/')
    def page():
        app.storage.browser['count'] = app.storage.browser.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.browser, 'count')

    @app.get('/count')
    def count():
        return 'count = ' + str(app.storage.browser['count'])

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')
    screen.open('/count')
    screen.should_contain('count = 3')  # also works with FastAPI endpoints


def test_browser_storage_supports_asyncio(screen: SeleniumScreen):
    @ui.page('/')
    async def page():
        app.storage.browser['count'] = app.storage.browser.get('count', 0) + 1
        await asyncio.sleep(0.5)
        ui.label(app.storage.browser['count'])

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('2')
    screen.switch_to(0)
    screen.open('/')
    screen.should_contain('3')


def test_browser_storage_modifications_after_page_load_are_forbidden(screen: SeleniumScreen):
    @ui.page('/')
    async def page():
        await ui.context.client.connected()
        try:
            app.storage.browser['test'] = 'data'
        except TypeError as e:
            ui.label(str(e))

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.should_contain('response to the browser has already been built')


def test_user_storage_modifications(screen: SeleniumScreen):
    @ui.page('/')
    async def page(delayed: bool = False):
        if delayed:
            await ui.context.client.connected()
        app.storage.user['count'] = app.storage.user.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.user, 'count')

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.should_contain('1')
    screen.open('/?delayed=True')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')


async def test_access_user_storage_from_fastapi(screen: SeleniumScreen):
    @app.get('/api')
    def api():
        app.storage.user['msg'] = 'yes'
        return 'OK'

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(f'http://localhost:{SeleniumScreen.PORT}/api')
        assert response.status_code == 200
        assert response.text == '"OK"'
        await asyncio.sleep(0.5)  # wait for storage to be written
        assert next(Path('.nicegui').glob('storage-user-*.json')).read_text('utf-8') == '{"msg":"yes"}'


def test_access_user_storage_on_interaction(screen: SeleniumScreen):
    @ui.page('/')
    async def page():
        if 'test_switch' not in app.storage.user:
            app.storage.user['test_switch'] = False
        ui.switch('switch').bind_value(app.storage.user, 'test_switch')

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.click('switch')
    screen.wait(0.5)
    assert next(Path('.nicegui').glob('storage-user-*.json')).read_text('utf-8') == '{"test_switch":true}'


def test_access_user_storage_from_button_click_handler(screen: SeleniumScreen):
    @ui.page('/')
    async def page():
        ui.button('test', on_click=app.storage.user.update(inner_function='works'))

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.click('test')
    screen.wait(1)
    assert next(Path('.nicegui').glob('storage-user-*.json')).read_text('utf-8') == '{"inner_function":"works"}'


async def test_access_user_storage_from_background_task(screen: SeleniumScreen):
    @ui.page('/')
    def page():
        async def subtask():
            await asyncio.sleep(0.1)
            app.storage.user['subtask'] = 'works'
        background_tasks.create(subtask())

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    assert next(Path('.nicegui').glob('storage-user-*.json')).read_text('utf-8') == '{"subtask":"works"}'


def test_user_and_general_storage_is_persisted(screen: SeleniumScreen):
    @ui.page('/')
    def page():
        app.storage.user['count'] = app.storage.user.get('count', 0) + 1
        app.storage.general['count'] = app.storage.general.get('count', 0) + 1
        ui.label(f'user: {app.storage.user["count"]}')
        ui.label(f'general: {app.storage.general["count"]}')

    screen.ui_run_kwargs['storage_secret'] = 'just a test'
    screen.open('/')
    screen.open('/')
    screen.open('/')
    screen.should_contain('user: 3')
    screen.should_contain('general: 3')
    screen.selenium.delete_all_cookies()
    screen.open('/')
    screen.should_contain('user: 1')
    screen.should_contain('general: 4')


def test_rapid_storage(screen: SeleniumScreen):
    # https://github.com/zauberzeug/nicegui/issues/1099
    ui.button('test', on_click=lambda: (
        app.storage.general.update(one=1),
        app.storage.general.update(two=2),
        app.storage.general.update(three=3),
    ))

    screen.open('/')
    screen.click('test')
    screen.wait(0.5)
    assert Path('.nicegui', 'storage-general.json').read_text('utf-8') == '{"one":1,"two":2,"three":3}'


def test_tab_storage_is_local(screen: SeleniumScreen):
    @ui.page('/')
    async def page():
        await context.client.connected()
        app.storage.tab['count'] = app.storage.tab.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.tab, 'count')

    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')

    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('1')

    screen.switch_to(0)
    screen.open('/')
    screen.should_contain('3')


def test_tab_storage_is_auto_removed(screen: SeleniumScreen):
    storage_module.PURGE_INTERVAL = 0.1
    app.storage.max_tab_storage_age = 0.5

    @ui.page('/')
    async def page():
        await context.client.connected()
        app.storage.tab['count'] = app.storage.tab.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.tab, 'count')

    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')

    screen.wait(1)
    screen.open('/')
    screen.should_contain('1')


def test_clear_tab_storage(screen: SeleniumScreen):
    storage_module.PURGE_INTERVAL = 60

    @ui.page('/')
    async def page():
        await context.client.connected()
        app.storage.tab['test'] = '123'
        ui.button('clear', on_click=app.storage.clear)

    screen.open('/')
    screen.should_contain('clear')

    tab_storages = app.storage._tabs  # pylint: disable=protected-access
    assert len(tab_storages) == 1
    assert next(iter(tab_storages.values())) == {'test': '123'}

    screen.click('clear')
    screen.wait(0.5)
    assert not tab_storages


def test_client_storage(screen: SeleniumScreen):
    def increment():
        app.storage.client['counter'] = app.storage.client['counter'] + 1

    @ui.page('/')
    def page():
        app.storage.client['counter'] = 123
        ui.button('Increment').on_click(increment)
        ui.label().bind_text(app.storage.client, 'counter')

    screen.open('/')
    screen.should_contain('123')
    screen.click('Increment')
    screen.wait_for('124')

    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('123')

    screen.switch_to(0)
    screen.should_contain('124')


def test_clear_client_storage(screen: SeleniumScreen):
    with pytest.raises(RuntimeError):  # no context (auto index)
        app.storage.client.clear()

    @ui.page('/')
    def page():
        app.storage.client['counter'] = 123
        app.storage.client.clear()
        assert app.storage.client == {}

    screen.open('/')
