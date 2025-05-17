from nicegui import ui
from nicegui.testing import Screen


def test_log(screen: Screen):
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
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C\nD')

    screen.open('/')
    assert screen.find_element(log).text == 'B\nC\nD'


def test_replace_log(screen: Screen):
    with ui.row() as container:
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
    log = ui.log()
    log.push('50%')
    ui.button('push', on_click=lambda: log.push('100%'))

    screen.open('/')
    screen.should_contain('50%')
    screen.click('push')
    screen.should_contain('100%')


def test_log_against_defaults(screen: Screen):

    ui.label.default_classes('text-gray-500')
    ui.label.default_style('font-size: 2rem')
    ui.label.default_props('my_label_props')

    log = ui.log()
    log.push('This is how a log label looks like',
             classes='text-red-500',
             style='font-size: 1rem',
             props='my_log_props',
             )

    screen.open('/')

    # for all divs, check if the default classes, style and props are applied, if so, fail
    for div in screen.find_all_by_tag('div'):
        props = div.get_attribute('props')
        if props is not None and 'my_label_props' in props:
            raise AssertionError(f'Default props should not be applied to log label: {div}')
        classes = div.get_attribute('class')
        if classes is not None and 'text-gray-500' in classes:
            raise AssertionError(f'Default classes should not be applied to log label: {div}')
        style = div.get_attribute('style')
        if style is not None and 'font-size: 2rem' in style:
            raise AssertionError(f'Default style should not be applied to log label: {div}')
