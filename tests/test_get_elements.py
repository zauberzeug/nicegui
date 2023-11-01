from nicegui import ui

from .screen import Screen


def test_get_all(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    elements = list(ui.get())

    screen.open('/')
    assert len(elements) == 8
    assert elements[0].tag == 'q-page-container'
    assert elements[1].tag == 'q-page'
    assert elements[2]._classes == ['nicegui-content']
    assert elements[3].text == 'button A'
    assert elements[4].text == 'label A'
    assert elements[5].__class__.__name__ == 'Row'
    assert elements[6].text == 'button B'
    assert elements[7].text == 'label B'


def test_get_by_text_element(screen: Screen):
    from nicegui.elements.mixins.text_element import TextElement

    ui.button('button A')
    ui.label('label A')
    ui.icon('home')
    ui.button('button B')
    ui.label('label B')

    result = [b.text for b in ui.get(type=TextElement)]

    screen.open('/')
    assert result == ['button A', 'label A', 'button B', 'label B']


def test_get_by_type(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = ', '.join(b.text for b in ui.get(type=ui.button))

    screen.open('/')
    assert result == 'button A, button B'


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


def test_get_by_key(screen: Screen):
    ui.button('button A')
    ui.button('button B').keys('important')

    result = list(ui.get(key='important'))

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button B'


def test_get_by_specific_key(screen: Screen):
    ui.button('button A').keys('test')
    ui.button('button B').keys('important ', 'test')
    ui.button('button C').keys(' important test')

    test = list(ui.get(key='test'))
    important = list(ui.get(key='important'))

    screen.open('/')
    assert len(test) == 3
    assert len(important) == 2
    assert test[0].text == 'button A'
    assert test[1].text == 'button B'
    assert test[2].text == 'button C'
    assert important[0].text == 'button B'
    assert important[1].text == 'button C'


def test_get_by_multiple_keys(screen: Screen):
    ui.button('button A').keys('test')
    ui.button('button B').keys('important ', 'test')
    ui.button('button C').keys(' important test')

    search = ui.get(type=ui.button, key='test important')
    result = [b.text for b in search]
    screen.open('/')
    assert result == ['button B', 'button C']


def test_get_within_type(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    result = [b.text for b in ui.get(type=ui.button).within(type=ui.row)]

    screen.open('/')
    assert result == ['button B']


def test_get_within_key(screen: Screen):
    ui.button('button A')
    ui.label('label A')
    with ui.row().keys('horizontal'):
        ui.button('button B')
        ui.label('label B')

    result = [b.text for b in ui.get().within(key='horizontal')]

    screen.open('/')
    assert result == ['button B', 'label B']
