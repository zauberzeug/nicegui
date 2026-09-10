import asyncio

from nicegui import Client, ui
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


async def test_awaited_run_javascript_resolves_when_client_is_deleted(user: User):
    """The task awaiting run_javascript must not time out or wait forever when the client is deleted, e.g. after a disconnect."""
    clients: list[Client] = []
    results = []

    @ui.page('/')
    async def page():
        clients.append(ui.context.client)
        results.append(await ui.run_javascript('window.innerWidth'))

    await user.http_client.get('/')  # request the page without ever opening the websocket
    await asyncio.sleep(0)
    assert not results

    Client.prune_instances(client_age_threshold=0)  # delete the client, waking up connected()
    await asyncio.sleep(0.1)  # let the page function resume
    assert results == [None]  # the page function resumed with None instead of timing out

    # calling on a deleted client resolves immediately
    assert await clients[0].run_javascript('window.innerWidth') is None
