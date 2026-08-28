import asyncio

from nicegui import background_tasks, ui
from nicegui.client import Client
from nicegui.testing import Screen, User


def test_run_javascript_on_button_press(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('change title', on_click=lambda: ui.run_javascript('document.title = "A New Title"'))

    screen.open('/')
    assert screen.selenium.title == 'NiceGUI'
    screen.click('change title')
    screen.wait(0.5)
    screen.should_contain('A New Title')


def test_run_javascript_on_value_change(screen: Screen):
    @ui.page('/')
    async def page():
        ui.radio(['A', 'B'], on_change=lambda e: ui.run_javascript(f'document.title = "Page {e.value}"'))
        await ui.context.client.connected()
        ui.run_javascript('document.title = "Initial Title"')

    screen.open('/')
    screen.wait(0.5)
    screen.should_contain('Initial Title')
    screen.click('A')
    screen.wait(0.5)
    screen.should_contain('Page A')
    screen.click('B')
    screen.wait(0.5)
    screen.should_contain('Page B')


def test_run_javascript_before_client_connected(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('before js')
        ui.run_javascript('document.title = "New Title"')
        ui.label('after js')

    screen.open('/')
    screen.should_contain('before js')
    screen.should_contain('after js')
    screen.wait(0.5)
    screen.should_contain('New Title')


def test_response_from_javascript(screen: Screen):
    @ui.page('/')
    def page():
        async def compute() -> None:
            response = await ui.run_javascript('1 + 41')
            ui.label(response)

        ui.button('compute', on_click=compute)

    screen.open('/')
    screen.click('compute')
    screen.should_contain('42')


def test_async_javascript(screen: Screen):
    @ui.page('/')
    def page():
        async def run():
            result = await ui.run_javascript('await new Promise(r => setTimeout(r, 100)); return 42')
            ui.label(result)

        ui.button('run', on_click=run)

    screen.open('/')
    screen.click('run')
    screen.should_contain('42')


def test_simultaneous_async_javascript(screen: Screen):
    @ui.page('/')
    def page():
        async def runA():
            result = await ui.run_javascript('await new Promise(r => setTimeout(r, 500)); return 1')
            ui.label(f'A: {result}')

        async def runB():
            result = await ui.run_javascript('await new Promise(r => setTimeout(r, 250)); return 2')
            ui.label(f'B: {result}')

        ui.button('runA', on_click=runA)
        ui.button('runB', on_click=runB)

    screen.open('/')
    screen.click('runA')
    screen.click('runB')
    screen.should_contain('A: 1')
    screen.should_contain('B: 2')


async def test_awaited_run_javascript_resolves_when_client_is_deleted_while_waiting(user: User):
    results = []

    @ui.page('/')
    async def page():
        results.append(await ui.run_javascript('window.innerWidth'))

    await user.http_client.get('/')  # request the page without ever opening the websocket
    await asyncio.sleep(0)
    Client.prune_instances(client_age_threshold=0)  # delete the client, waking up connected()
    await asyncio.sleep(1.5)  # longer than run_javascript's default 1.0 s timeout
    assert results == [None]


async def test_awaited_run_javascript_resolves_when_client_is_already_deleted(user: User):
    results = []

    @ui.page('/')
    async def page():
        client = ui.context.client

        async def later() -> None:
            await asyncio.sleep(0.3)  # resume long after the client is gone
            results.append(await client.run_javascript('window.innerWidth'))

        background_tasks.create(later())

    await user.http_client.get('/')  # request the page without ever opening the websocket
    await asyncio.sleep(0)
    Client.prune_instances(client_age_threshold=0)
    await asyncio.sleep(1.5)
    assert results == [None]
