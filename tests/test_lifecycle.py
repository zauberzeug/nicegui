from nicegui import ui

from .screen import Screen


def test_adding_elements_during_onconnect(screen: Screen):
    ui.label('Label 1')
    ui.on_connect(lambda: ui.label('Label 2'))

    screen.open('/')
    screen.should_contain('Label 2')
