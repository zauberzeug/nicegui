from nicegui import ui
from nicegui.testing import Screen


def test_clipboard(screen: Screen):
    ui.button('Copy to clipboard', on_click=lambda: ui.clipboard.write('Hello, World!'))

    async def read_clipboard():
        ui.notify('Clipboard: ' + await ui.clipboard.read())
    ui.button('Read from clipboard', on_click=read_clipboard)

    screen.open('/')
    screen.selenium.set_permissions('clipboard-read', 'granted')
    screen.selenium.set_permissions('clipboard-write', 'granted')

    screen.click('Copy to clipboard')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return navigator.clipboard.readText()') == 'Hello, World!'

    screen.click('Read from clipboard')
    screen.should_contain('Clipboard: Hello, World!')
