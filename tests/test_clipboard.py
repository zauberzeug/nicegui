from nicegui import ui
from nicegui.testing import SharedScreen


def test_clipboard(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Copy to clipboard', on_click=lambda: ui.clipboard.write('Hello, World!'))

        async def read_clipboard():
            ui.notify('Clipboard: ' + await ui.clipboard.read())
        ui.button('Read from clipboard', on_click=read_clipboard)

    shared_screen.open('/')
    shared_screen.selenium.set_permissions('clipboard-read', 'granted')
    shared_screen.selenium.set_permissions('clipboard-write', 'granted')

    shared_screen.click('Copy to clipboard')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script('return navigator.clipboard.readText()') == 'Hello, World!'

    shared_screen.click('Read from clipboard')
    shared_screen.should_contain('Clipboard: Hello, World!')
