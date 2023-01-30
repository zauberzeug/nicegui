from nicegui import ui

from .screen import Screen


def test_time(screen: Screen):
    t = ui.time(value='01:23')
    ui.label().bind_text_from(t, 'value')

    screen.open('/')
    screen.should_contain('01:23')

    screen.click('8')
    screen.wait(0.1)
    screen.should_contain('08:23')

    screen.click('45')
    screen.wait(0.1)
    screen.should_contain('08:45')

    screen.click('PM')
    screen.wait(0.1)
    screen.should_contain('20:45')
