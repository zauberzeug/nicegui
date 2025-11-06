from nicegui import ui
from nicegui.testing import Screen


def test_log(screen: Screen):
    log = None

    @ui.page('/')
    def page():
        nonlocal log
        log = ui.log(max_lines=3)
        log.push('A')
        log.push('B')
        log.push('C')
        log.push('D')

    screen.open('/')
    assert screen.find_element(log).text == 'B\nC\nD'

    log.clear()
    screen.wait(0.5)
    assert screen.find_element(log).text == ''


def test_log_with_newlines(screen: Screen):
    log = None

    @ui.page('/')
    def page():
        nonlocal log
        log = ui.log(max_lines=3)
        log.push('A')
        log.push('B')
        log.push('C\nD')

    screen.open('/')
    assert screen.find_element(log).text == 'B\nC\nD'


def test_replace_log(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row().classes('w-full') as container:
            ui.log().push('A')

        def replace():
            container.clear()
            with container:
                ui.log().push('B')
        ui.button('Replace', on_click=replace)

    screen.open('/')
    screen.should_contain('A')

    screen.click('Replace')
    screen.should_contain('B')
    screen.should_not_contain('A')


def test_special_characters(screen: Screen):
    @ui.page('/')
    def page():
        log = ui.log()
        log.push('50%')
        ui.button('push', on_click=lambda: log.push('100%'))

    screen.open('/')
    screen.should_contain('50%')

    screen.click('push')
    screen.should_contain('100%')


def test_log_against_defaults(screen: Screen):
    @ui.page('/')
    def page():
        ui.label.default_classes('text-red')
        ui.label.default_style('margin: 1rem')
        ui.label.default_props('my-prop=A')

        log = ui.log()
        log.push('Log line', classes='text-green', style='margin: 2rem', props='my-prop=B')

    screen.open('/')
    line = screen.find('Log line')
    assert line.get_attribute('my-prop') == 'B'
    assert line.get_attribute('class') == 'text-green'
    assert line.get_attribute('style') == 'margin: 2rem;'
