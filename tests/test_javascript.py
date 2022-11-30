import pytest

from nicegui import Client, ui
from nicegui.events import ValueChangeEventArguments

from .screen import Screen


def test_run_javascript_on_button_press(screen: Screen):
    async def set_title() -> None:
        await ui.run_javascript('document.title = "A New Title"')
    ui.button('change title', on_click=set_title)

    screen.open('/')
    assert screen.selenium.title == 'NiceGUI'
    screen.click('change title')
    assert screen.selenium.title == 'A New Title'
    assert screen.selenium.title != 'NiceGUI'


def test_run_javascript_on_value_change(screen: Screen):
    @ui.page('/')
    async def main_page(client: Client):
        async def set_title(e: ValueChangeEventArguments) -> None:
            await ui.run_javascript(f'document.title = "{e.value}"')
        ui.radio(['Page Title A', 'Page Title B'], on_change=set_title)
        await client.handshake()
        await ui.run_javascript('document.title = "Initial Page Title"')

    screen.open('/')
    screen.wait(0.3)
    assert screen.selenium.title == 'Initial Page Title'
    screen.click('Title B')
    screen.wait(0.3)
    assert screen.selenium.title == 'Page Title B'
    screen.click('Title A')
    screen.wait(0.3)
    assert screen.selenium.title == 'Page Title A'


def test_run_javascript_before_client_handshake(screen: Screen):
    @ui.page('/')
    async def page():
        ui.label('before js')
        with pytest.raises(RuntimeError):
            await ui.run_javascript('document.title = "A New Title"')
        ui.label('after js')

    screen.open('/')
    assert screen.selenium.title == 'NiceGUI'
    screen.should_contain('before js')
    screen.should_contain('after js')


def test_response_from_javascript(screen: Screen):
    async def compute() -> None:
        response = await ui.run_javascript('1 + 41')
        for _, answer in response.items():
            ui.label(answer)

    ui.button('compute', on_click=compute)

    screen.open('/')
    screen.click('compute')
    screen.should_contain('42')
