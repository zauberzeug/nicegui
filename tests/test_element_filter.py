from typing import List

import pytest

from nicegui import ElementFilter, ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.testing import User

pytestmark = pytest.mark.usefixtures('user')

# pylint: disable=missing-function-docstring


def texts(element_filter: ElementFilter) -> List[str]:
    return [element.text for element in element_filter]


def test_find_all() -> None:
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    elements: List[ui.element] = list(ElementFilter())
    assert len(elements) == 8
    assert elements[0].tag == 'q-page-container'
    assert elements[1].tag == 'q-page'
    assert elements[2].classes == ['nicegui-content']
    assert elements[3].text == 'button A'  # type: ignore
    assert elements[4].text == 'label A'  # type: ignore
    assert elements[5].__class__ == ui.row
    assert elements[6].text == 'button B'  # type: ignore
    assert elements[7].text == 'label B'  # type: ignore


def test_find_kind():
    ui.icon('home')
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(kind=ui.button)) == ['button A', 'button B']
    assert texts(ElementFilter(kind=TextElement)) == ['button A', 'label A', 'button B', 'label B']


def test_find_content():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(content='A')) == ['button A', 'label A']
    assert texts(ElementFilter(content=['A', 'butt'])) == ['button A']


def test_find_radio():
    radio_list = ui.radio(['radio 1', 'radio 2'])
    radio_dict = ui.radio({'radio 1': 'Radio A', 'radio 2': 'Radio B'})

    assert next(iter(ElementFilter(content=['radio 1']))) is radio_list
    assert next(iter(ElementFilter(content=['Radio A']))) is radio_dict


def test_find_toggle():
    toggle_list = ui.toggle(['toggle 1', 'toggle 2'])
    toggle_dict = ui.toggle({'toggle 1': 'Toggle A', 'toggle 2': 'Toggle B'})

    assert next(iter(ElementFilter(content=['toggle 1']))) is toggle_list
    assert next(iter(ElementFilter(content=['Toggle A']))) is toggle_dict


def test_find_select():
    select_list = ui.select(['select 1', 'select 2'])
    select_dict = ui.select({'select 1': 'Select A', 'select 2': 'Select B'})

    select_list._is_showing_popup = True  # pylint: disable=protected-access
    select_dict._is_showing_popup = True  # pylint: disable=protected-access

    assert next(iter(ElementFilter(content=['select 1']))) is select_list
    assert next(iter(ElementFilter(content=['Select A']))) is select_dict


def test_find_marker():
    ui.button('button A')
    ui.button('button B').mark('important')
    ui.button('button C').mark('important ', 'foo')
    ui.button('button D').mark(' important bar')

    assert texts(ElementFilter(marker='important')) == ['button B', 'button C', 'button D']
    assert texts(ElementFilter(marker='foo')) == ['button C']
    assert texts(ElementFilter(marker='bar important')) == ['button D']
    assert texts(ElementFilter(marker='important bar')) == ['button D']


def test_find_within_marker():
    ui.button('button A')
    ui.label('label A')
    with ui.row().mark('horizontal'):
        ui.button('button B')
        ui.label('label B')
        with ui.column().mark('vertical'):
            ui.button('button C')
            ui.label('label C')

    assert texts(ElementFilter(kind=ui.button).within(marker='horizontal')) == ['button B', 'button C']
    assert texts(ElementFilter(kind=ui.button).within(marker='horizontal vertical')) == ['button C']
    assert texts(ElementFilter(kind=ui.button).not_within(marker='horizontal')) == ['button A']
    assert texts(ElementFilter(kind=ui.button).not_within(marker='horizontal vertical')) == ['button A']


def test_find_within_marker2():
    with ui.row().mark('a b'):
        ui.label('Label 1')
    with ui.row().mark('a'):
        ui.label('Label 2')
    ui.label('Label 3')

    assert texts(ElementFilter(kind=ui.label).within(marker='a b')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='b a')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='b')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='a')) == ['Label 1', 'Label 2']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='a b')) == ['Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='b a')) == ['Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='b')) == ['Label 2', 'Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='a')) == ['Label 3']


def test_find_within_instance():
    ui.button('button A')
    ui.label('label A')
    with ui.row() as row:
        ui.button('button B')
        ui.label('label B')
        with ui.column() as column1:
            ui.button('button C')
            ui.label('label C')
        with ui.column() as column2:
            ui.button('button D')
            ui.label('label D')

    assert texts(ElementFilter(kind=ui.button).within(instance=row)) == ['button B', 'button C', 'button D']
    assert texts(ElementFilter(kind=ui.button).within(instance=[row, column1])) == ['button C']
    assert texts(ElementFilter(kind=ui.button).within(instance=[column1, column2])) == []
    assert texts(ElementFilter(kind=ui.button).not_within(instance=row)) == ['button A']


def test_find_within_kind():
    ui.button('button A')
    with ui.row():
        ui.label('label A')
        ui.button('button B')
        ui.label('label B')
    with ui.column():
        ui.label('label C')
        with ui.card():
            ui.button('button C')

    assert texts(ElementFilter(content='B').within(kind=ui.row)) == ['button B', 'label B']
    assert texts(ElementFilter(content='C').within(kind=ui.column)) == ['label C', 'button C']
    assert texts(ElementFilter(content='C').within(kind=ui.column).within(kind=ui.card)) == ['button C']
    assert texts(ElementFilter(kind=ui.button).not_within(kind=ui.row)) == ['button A', 'button C']


def test_find_exclude_kind():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(content='A').exclude(kind=ui.label)) == ['button A']


def test_find_exclude_marker():
    ui.button('button A').mark('normal')
    ui.label('label A').mark('important')
    ui.button('button B')
    ui.label('label B').mark('normal')

    assert texts(ElementFilter(kind=TextElement).exclude(marker='normal')) == ['label A', 'button B']


def test_find_exclude_content():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(kind=ui.button).exclude(content='A')) == ['button B']


def test_find_in_local_scope():
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')
        assert texts(ElementFilter(local_scope=True)) == ['button B', 'label B']


async def test_setting_classes(user: User):
    ui.label('label A')
    ui.label('label B')

    ElementFilter(kind=ui.label).classes('text-2xl')

    await user.open('/')
    for label in user.find('label').elements:
        assert label.classes == ['text-2xl']


async def test_setting_style(user: User):
    ui.label('label A')
    ui.label('label B')

    ElementFilter(kind=ui.label).style('color: red')

    await user.open('/')
    for label in user.find('label').elements:
        assert label.style['color'] == 'red'


async def test_setting_props(user: User):
    ui.button('button A')
    ui.button('button B')

    ElementFilter(kind=ui.button).props('flat')

    await user.open('/')
    for button in user.find('button').elements:
        assert button.props['flat']


async def test_typing(user: User):
    ui.button('button A')
    ui.label('label A')

    await user.open('/')
    # NOTE we have not yet found a way to test the typing suggestions automatically
    # to test, hover over the variable and verify that your IDE infers the correct type
    _ = ElementFilter(kind=ui.button)  # ElementFilter[ui.button]
    _ = ElementFilter(kind=ui.label)  # ElementFilter[ui.label]
    _ = ElementFilter()  # ElementFilter[Element]
