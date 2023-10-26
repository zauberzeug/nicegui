from nicegui import ui

from .screen import Screen


def test_min(screen: Screen):

    ui.pagination(min=1, max=10)

    screen.open('/')
    screen.click('1')

def test_max(screen: Screen):

    ui.pagination(min=1, max=10)

    screen.open('/')
    screen.click('10')