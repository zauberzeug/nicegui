from nicegui import ui
from nicegui.testing import SharedScreen


def test_log(shared_screen: SharedScreen):
    log = None

    @ui.page('/')
    def page():
        nonlocal log
        log = ui.log(max_lines=3)
        log.push('A')
        log.push('B')
        log.push('C')
        log.push('D')

    shared_screen.open('/')
    assert shared_screen.find_element(log).text == 'B\nC\nD'

    log.clear()
    shared_screen.wait(0.5)
    assert shared_screen.find_element(log).text == ''


def test_log_with_newlines(shared_screen: SharedScreen):
    log = None

    @ui.page('/')
    def page():
        nonlocal log
        log = ui.log(max_lines=3)
        log.push('A')
        log.push('B')
        log.push('C\nD')

    shared_screen.open('/')
    assert shared_screen.find_element(log).text == 'B\nC\nD'


def test_replace_log(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row().classes('w-full') as container:
            ui.log().push('A')

        def replace():
            with container.clear():
                ui.log().push('B')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    shared_screen.should_contain('A')

    shared_screen.click('Replace')
    shared_screen.should_contain('B')
    shared_screen.should_not_contain('A')


def test_special_characters(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        log = ui.log()
        log.push('50%')
        ui.button('push', on_click=lambda: log.push('100%'))

    shared_screen.open('/')
    shared_screen.should_contain('50%')

    shared_screen.click('push')
    shared_screen.should_contain('100%')


def test_log_against_defaults(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label.default_classes('text-red')
        ui.label.default_style('margin: 1rem')
        ui.label.default_props('my-prop=A')

        log = ui.log()
        log.push('Log line', classes='text-green', style='margin: 2rem', props='my-prop=B')

    shared_screen.open('/')
    line = shared_screen.find('Log line')
    assert line.get_attribute('my-prop') == 'B'
    assert line.get_attribute('class') == 'text-green'
    assert line.get_attribute('style') == 'margin: 2rem;'
