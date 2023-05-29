import asyncio

from nicegui import Client, app, ui

from .screen import Screen


def test_browser_data_is_stored_in_the_browser(screen: Screen):
    @ui.page('/')
    def page():
        app.storage.browser['count'] = app.storage.browser.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.browser, 'count')

    @app.get('/count')
    def count():
        return 'count = ' + str(app.storage.browser['count'])

    screen.open('/')
    screen.should_contain('1')
    screen.open('/')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')
    screen.open('/count')
    screen.should_contain('count = 3')  # also works with FastAPI endpoints


def test_browser_storage_supports_asyncio(screen: Screen):
    @ui.page('/')
    async def page():
        app.storage.browser['count'] = app.storage.browser.get('count', 0) + 1
        await asyncio.sleep(0.5)
        ui.label(app.storage.browser['count'])

    screen.open('/')
    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('2')
    screen.switch_to(0)
    screen.open('/')
    screen.should_contain('3')


def test_browser_storage_modifications_after_page_load_are_forbidden(screen: Screen):
    @ui.page('/')
    async def page(client: Client):
        await client.connected()
        try:
            app.storage.browser['test'] = 'data'
        except TypeError as e:
            ui.label(str(e))

    screen.open('/')
    screen.should_contain('response to the browser has already been build')


def test_individual_storage_modifications(screen: Screen):
    @ui.page('/')
    async def page(client: Client, delayed: bool = False):
        if delayed:
            await client.connected()
        app.storage.individual['count'] = app.storage.individual.get('count', 0) + 1
        ui.label().bind_text_from(app.storage.individual, 'count')

    screen.open('/')
    screen.should_contain('1')
    screen.open('/?delayed=True')
    screen.should_contain('2')
    screen.open('/')
    screen.should_contain('3')


def test_individual_and_general_storage_is_persisted(screen: Screen):
    @ui.page('/')
    def page():
        app.storage.individual['count'] = app.storage.individual.get('count', 0) + 1
        app.storage.general['count'] = app.storage.general.get('count', 0) + 1
        ui.label(f'individual: {app.storage.individual["count"]}')
        ui.label(f'general: {app.storage.general["count"]}')
        ui.button('backup', on_click=app.storage.backup)

    screen.open('/')
    screen.open('/')
    screen.open('/')
    screen.should_contain('individual: 3')
    screen.should_contain('general: 3')
    screen.click('backup')
    screen.selenium.delete_all_cookies()
    screen.open('/')
    screen.should_contain('individual: 1')
    screen.should_contain('general: 4')
