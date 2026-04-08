from nicegui import ui
from nicegui.testing import Screen


def test_skip_to_main(screen: Screen):
    target = None

    @ui.page('/')
    def page():
        nonlocal target
        ui.skip_to_main()
        target = ui.label('Main content')

    screen.open('/')
    button = screen.find_by_class('nicegui-skip-to-main')
    assert button.get_attribute('innerText') == 'Skip to main content'
    assert button.get_attribute('data-target') == str(target.id)

    screen.selenium.execute_script('arguments[0].focus(); arguments[0].click();', button)
    screen.wait(0.5)
    assert screen.selenium.switch_to.active_element.get_attribute('id') == f'c{target.id}'


def test_context_manager(screen: Screen):
    after = None

    @ui.page('/')
    def page():
        nonlocal after
        with ui.skip_to_main():
            ui.label('Jump to content')
        after = ui.button('After skip')

    screen.open('/')
    button = screen.find_by_class('nicegui-skip-to-main')
    assert 'Jump to content' in button.get_attribute('innerText')
    assert button.get_attribute('data-target') == str(after.id)
