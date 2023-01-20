from nicegui import ui

from .screen import Screen


def test_date(screen: Screen):
    ui.date(value='2023-01-01')

    screen.open('/')
    screen.should_contain('Sun, Jan 1')

    screen.click('31')
    screen.should_contain('Tue, Jan 31')
