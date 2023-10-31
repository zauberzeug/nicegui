from nicegui import ui

from .screen import Screen


def test_get_by_type(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    ui.label(', '.join([b.text for b in ui.get(type=ui.button)]))

    screen.open('/')
    screen.should_contain('button A, button B')
