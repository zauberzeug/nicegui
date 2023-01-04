from nicegui import ui

from .screen import Screen


def test_adding_elements_during_onconnect(screen: Screen):
    ui.label('Label 1')
    ui.on_connect(lambda: ui.label('Label 2'))

    screen.open('/')
    screen.should_contain('Label 2')


def test_async_connect_handler(screen: Screen):
    async def run_js():
        result.text = await ui.run_javascript('41 + 1')
    result = ui.label()
    ui.on_connect(run_js)

    screen.open('/')
    screen.should_contain('42')
