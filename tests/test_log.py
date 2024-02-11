from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_log(screen: SeleniumScreen):
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


def test_log_with_newlines(screen: SeleniumScreen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C\nD')

    screen.open('/')
    assert screen.find_element(log).text == 'B\nC\nD'


def test_replace_log(screen: SeleniumScreen):
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


def test_special_characters(screen: SeleniumScreen):
    log = ui.log()
    log.push('50%')
    ui.button('push', on_click=lambda: log.push('100%'))

    screen.open('/')
    screen.should_contain('50%')
    screen.click('push')
    screen.should_contain('100%')


def test_line_duplication_bug_906(screen: SeleniumScreen):
    ui.button('Log', on_click=lambda: ui.log().push('Hi!'))

    screen.open('/')
    screen.click('Log')
    screen.should_contain('Hi!')
    screen.should_not_contain('Hi!\nHi!')


def test_another_duplication_bug_1173(screen: SeleniumScreen):
    log1 = ui.log()

    def test():
        log1.push('A')
        log2 = ui.log()
        log2.push('C')
        log2.push('D')
    ui.button('test', on_click=test)

    screen.open('/')
    screen.click('test')
    screen.should_contain('A')
    screen.should_contain('C\nD')
    screen.should_not_contain('C\nD\nC\nD')
