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


def test_setting_classes(screen: Screen):
    ui.label('label A')
    ui.label('label B')

    ui.get(type=ui.label).classes('text-2xl')

    screen.open('/')
    assert screen.find('label A').get_attribute('class') == 'text-2xl'
    assert screen.find('label B').get_attribute('class') == 'text-2xl'


def test_setting_style(screen: Screen):
    ui.label('label A')
    ui.label('label B')

    ui.get(type=ui.label).style('color: red')

    screen.open('/')
    assert screen.find('label A').get_attribute('style') == 'color: red;'
    assert screen.find('label B').get_attribute('style') == 'color: red;'


def test_setting_props(screen: Screen):
    ui.button('A')
    ui.button('B')

    ui.get(type=ui.button).props('flat')

    screen.open('/')
    for e in screen.find_all_by_tag('button'):
        assert 'q-btn--flat' in e.get_attribute('class')
