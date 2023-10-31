from nicegui import ui

from .screen import Screen


def test_get_all(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    elements = [str(b) for b in ui.get()]

    screen.open('/')
    assert len(elements) == 8
    assert elements[0] == '<q-page-container>'
    assert elements[1] == '<q-page>'
    assert elements[2] == '<div classes="nicegui-content">'
    assert elements[3] == '<Button text="button A">'
    assert elements[4] == '<Label text="label A">'
    assert elements[5] == '<Row classes="nicegui-row, wrap">'
    assert elements[6] == '<Button text="button B">'
    assert elements[7] == '<Label text="label B">'


def test_get_by_type(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    ui.label(', '.join(b.text for b in ui.get(type=ui.button)))

    screen.open('/')
    screen.should_contain('button A, button B')
