from nicegui import ui
from nicegui.testing import SharedScreen


def test_run_javascript_on_button_press(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('change title', on_click=lambda: ui.run_javascript('document.title = "A New Title"'))

    shared_screen.open('/')
    assert shared_screen.selenium.title == 'NiceGUI'
    shared_screen.click('change title')
    shared_screen.wait(0.5)
    shared_screen.should_contain('A New Title')


def test_run_javascript_on_value_change(shared_screen: SharedScreen):
    @ui.page('/')
    async def page():
        ui.radio(['A', 'B'], on_change=lambda e: ui.run_javascript(f'document.title = "Page {e.value}"'))
        await ui.context.client.connected()
        ui.run_javascript('document.title = "Initial Title"')

    shared_screen.open('/')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Initial Title')
    shared_screen.click('A')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Page A')
    shared_screen.click('B')
    shared_screen.wait(0.5)
    shared_screen.should_contain('Page B')


def test_run_javascript_before_client_connected(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('before js')
        ui.run_javascript('document.title = "New Title"')
        ui.label('after js')

    shared_screen.open('/')
    shared_screen.should_contain('before js')
    shared_screen.should_contain('after js')
    shared_screen.wait(0.5)
    shared_screen.should_contain('New Title')


def test_response_from_javascript(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def compute() -> None:
            response = await ui.run_javascript('1 + 41')
            ui.label(response)

        ui.button('compute', on_click=compute)

    shared_screen.open('/')
    shared_screen.click('compute')
    shared_screen.should_contain('42')


def test_async_javascript(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        async def run():
            result = await ui.run_javascript('await new Promise(r => setTimeout(r, 100)); return 42')
            ui.label(result)

        ui.button('run', on_click=run)

    shared_screen.open('/')
    shared_screen.click('run')
    shared_screen.should_contain('42')


def test_simultaneous_async_javascript(shared_screen: SharedScreen):
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

    shared_screen.open('/')
    shared_screen.click('runA')
    shared_screen.click('runB')
    shared_screen.should_contain('A: 1')
    shared_screen.should_contain('B: 2')
