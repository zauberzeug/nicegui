import pytest

from nicegui import ui

from .screen import Screen


def test_log(screen: Screen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C')
    log.push('D')

    screen.open('/')
    assert screen.find_by_id(log.id).text == 'B\nC\nD'

    log.clear()
    screen.wait(0.5)
    assert screen.find_by_id(log.id).text == ''


def test_log_with_newlines(screen: Screen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C\nD')

    screen.open('/')
    assert screen.find_by_id(log.id).text == 'B\nC\nD'


@pytest.mark.skip(reason='issue #600')
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
