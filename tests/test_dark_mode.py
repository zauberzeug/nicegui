from nicegui import ui
from nicegui.testing import Screen


def test_dark_mode(screen: Screen):
    ui.label('Hello')
    dark = ui.dark_mode()
    ui.button('Dark', on_click=dark.enable)
    ui.button('Light', on_click=dark.disable)
    ui.button('Auto', on_click=dark.auto)
    ui.button('Toggle', on_click=dark.toggle)

    def assert_dark(value: bool) -> None:
        classes = (screen.find_by_tag('body').get_attribute('class') or '').split()
        assert ('body--dark' in classes) == value
        assert ('body--light' in classes) != value

    screen.open('/')
    screen.should_contain('Hello')
    assert_dark(False)

    screen.click('Dark')
    screen.wait(0.5)
    assert_dark(True)

    screen.click('Auto')
    screen.wait(0.5)
    assert_dark(False)

    screen.click('Toggle')
    screen.wait(0.5)
    screen.assert_py_logger('ERROR', 'Cannot toggle dark mode when it is set to auto.')

    screen.click('Light')
    screen.wait(0.5)
    assert_dark(False)

    screen.click('Toggle')
    screen.wait(0.5)
    assert_dark(True)
