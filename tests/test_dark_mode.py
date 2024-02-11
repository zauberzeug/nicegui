from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_dark_mode(screen: SeleniumScreen):
    ui.label('Hello')
    dark = ui.dark_mode()
    ui.button('Dark', on_click=dark.enable)
    ui.button('Light', on_click=dark.disable)
    ui.button('Auto', on_click=dark.auto)
    ui.button('Toggle', on_click=dark.toggle)

    screen.open('/')
    screen.should_contain('Hello')
    assert screen.find_by_tag('body').get_attribute('class') == 'desktop no-touch body--light'

    screen.click('Dark')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('class') == 'desktop no-touch body--dark dark'

    screen.click('Auto')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('class') == 'desktop no-touch body--light'

    screen.click('Toggle')
    screen.wait(0.5)
    screen.assert_py_logger('ERROR', 'Cannot toggle dark mode when it is set to auto.')

    screen.click('Light')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('class') == 'desktop no-touch body--light'

    screen.click('Toggle')
    screen.wait(0.5)
    assert screen.find_by_tag('body').get_attribute('class') == 'desktop no-touch body--dark dark'
