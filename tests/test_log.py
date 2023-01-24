from nicegui import ui

from .screen import Screen


def test_log(screen: Screen):
    log = ui.log(max_lines=3)
    log.push('A')
    log.push('B')
    log.push('C')
    log.push('D')

    screen.open('/')
    screen.should_not_contain('A')
    screen.should_contain('B')
    screen.should_contain('C')
    screen.should_contain('D')
