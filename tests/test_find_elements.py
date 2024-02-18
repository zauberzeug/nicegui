from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_get_all(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    elements = list(ui.find())

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


def test_get_by_text_element(screen: SeleniumScreen):
    from nicegui.elements.mixins.text_element import TextElement

    ui.button('button A')
    ui.label('label A')
    ui.icon('home')
    ui.button('button B')
    ui.label('label B')

    result = [b.text for b in ui.find(type=TextElement)]

    screen.open('/')
    assert result == ['button A', 'label A', 'button B', 'label B']


def test_get_by_type(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = ', '.join(b.text for b in ui.find(type=ui.button))

    screen.open('/')
    assert result == 'button A, button B'


def test_get_by_containing_text(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = ', '.join(b.text for b in ui.find(text='A'))

    screen.open('/')
    assert result == 'button A, label A'


def test_get_by_containing_texts(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = ', '.join(b.text for b in ui.find(text=['A', 'tt']))

    screen.open('/')
    assert result == 'button A'


def test_setting_classes(screen: SeleniumScreen):
    ui.label('label A')
    ui.label('label B')

    ui.find(type=ui.label).classes('text-2xl')

    screen.open('/')
    assert screen.find('label A').get_attribute('class') == 'text-2xl'
    assert screen.find('label B').get_attribute('class') == 'text-2xl'


def test_setting_style(screen: SeleniumScreen):
    ui.label('label A')
    ui.label('label B')

    ui.find(type=ui.label).style('color: red')

    screen.open('/')
    assert screen.find('label A').get_attribute('style') == 'color: red;'
    assert screen.find('label B').get_attribute('style') == 'color: red;'


def test_setting_props(screen: SeleniumScreen):
    ui.button('A')
    ui.button('B')

    ui.find(type=ui.button).props('flat')

    screen.open('/')
    for e in screen.find_all_by_tag('button'):
        assert 'q-btn--flat' in e.get_attribute('class')


def test_get_by_key(screen: SeleniumScreen):
    ui.button('button A')
    ui.button('button B').keys('important')

    result = list(ui.find(key='important'))

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button B'


def test_get_by_specific_key(screen: SeleniumScreen):
    ui.button('button A').keys('test')
    ui.button('button B').keys('important ', 'test')
    ui.button('button C').keys(' important test')

    test = list(ui.find(key='test'))
    important = list(ui.find(key='important'))

    screen.open('/')
    assert len(test) == 3
    assert len(important) == 2
    assert test[0].text == 'button A'
    assert test[1].text == 'button B'
    assert test[2].text == 'button C'
    assert important[0].text == 'button B'
    assert important[1].text == 'button C'


def test_get_by_multiple_keys(screen: SeleniumScreen):
    ui.button('button A').keys('test')
    ui.button('button B').keys('important ', 'test')
    ui.button('button C').keys(' important test')

    search = ui.find(type=ui.button, key='test important')
    result = [b.text for b in search]
    screen.open('/')
    assert result == ['button B', 'button C']


def test_get_within_type(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    result = [b.text for b in ui.find(type=ui.button).within(type=ui.row)]

    screen.open('/')
    assert result == ['button B']


def test_get_within_key(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row().keys('horizontal'):
        ui.button('button B')
        ui.label('label B')

    result = [e.text for e in ui.find().within(key='horizontal')]

    screen.open('/')
    assert result == ['button B', 'label B']


def test_get_within_element(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    result = [e.text for e in ui.find().within(element=r)]

    screen.open('/')
    assert result == ['button B', 'label B']


def test_get_within_elements(screen: SeleniumScreen):
    with ui.row() as r1:
        ui.button('button A')
        ui.label('label A')
    with ui.row() as r2:
        ui.button('button B')
        ui.label('label B')

    result = [e.text for e in ui.find().within(element=[r1, r2])]

    screen.open('/')
    assert result == ['button A', 'label A', 'button B', 'label B']


def test_get_with_excluding_type(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [e for e in ui.find(text='A').exclude(type=ui.label)]

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button A'


def test_get_with_excluding_key(screen: SeleniumScreen):
    ui.button('button A').keys('normal')
    ui.label('label A').keys('important')
    ui.button('button B')
    ui.label('label B').keys('normal')

    result = [e for e in ui.find(text=[' ']).exclude(key='normal')]

    screen.open('/')
    assert len(result) == 2
    assert result[0].text == 'label A'
    assert result[1].text == 'button B'


def test_get_with_excluding_text(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [e for e in ui.find(type=ui.button).exclude(text='A')]

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button B'


def test_get_not_within_type(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    result = [e for e in ui.find(type=ui.button).not_within(type=ui.row)]

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button A'


def test_get_not_within_key(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row().keys('horizontal'):
        ui.button('button B')
        ui.label('label B')

    result = [e for e in ui.find(type=ui.button).not_within(key='horizontal')]

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button A'


def test_get_not_within_element(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    result = [e for e in ui.find(type=ui.button).not_within(element=r)]

    screen.open('/')
    assert len(result) == 1
    assert result[0].text == 'button A'


def test_get_in_local_scope(screen: SeleniumScreen):
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')
        result = [e.text for e in ui.find(local_scope=True)]

    screen.open('/')
    assert result == ['button B', 'label B']
