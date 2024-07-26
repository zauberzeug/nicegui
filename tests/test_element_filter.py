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
    assert elements[2]._classes == ['nicegui-content']  # pylint: disable=protected-access
    assert elements[3].text == 'button A'  # type: ignore
    assert elements[4].text == 'label A'  # type: ignore
    assert elements[5].__class__ == ui.row
    assert elements[6].text == 'button B'  # type: ignore
    assert elements[7].text == 'label B'  # type: ignore


def test_find_by_text_element():
    ui.button('button A')
    ui.label('label A')
    ui.icon('home')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(kind=TextElement)) == ['button A', 'label A', 'button B', 'label B']


def test_find_by_kind():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(kind=ui.button)) == ['button A', 'button B']


def test_find_by_containing_text():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(content='A')) == ['button A', 'label A']


def test_find_by_containing_texts():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(content=['A', 'tt'])) == ['button A']


def test_find_by_marker():
    ui.button('button A')
    ui.button('button B').mark('important')

    assert texts(ElementFilter(marker='important')) == ['button B']


def test_find_by_specific_marker():
    ui.button('button A').mark('test')
    ui.button('button B').mark('important ', 'test')
    ui.button('button C').mark(' important test')

    assert texts(ElementFilter(marker='test')) == ['button A', 'button B', 'button C']
    assert texts(ElementFilter(marker='important')) == ['button B', 'button C']


def test_find_by_multiple_markers():
    ui.button('button A').mark('test')
    ui.button('button B').mark('important ', 'test')
    ui.button('button C').mark(' important test')

    assert texts(ElementFilter(marker='test important')) == ['button B', 'button C']


def test_find_within_marker():
    ui.button('button A')
    ui.label('label A')
    with ui.row().mark('horizontal'):
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter().within(marker='horizontal')) == ['button B', 'label B']


def test_find_within_element():
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter().within(instance=r)) == ['button B', 'label B']


def test_find_within_elements():
    with ui.row() as row1:
        ui.button('button A')
        ui.label('label A')
    with ui.row() as row2:
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter().within(instance=[row1, row2])) == ['button A', 'label A', 'button B', 'label B']


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


def test_find_with_excluding_kind():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(content='A').exclude(kind=ui.label)) == ['button A']


def test_find_with_excluding_marker():
    ui.button('button A').mark('normal')
    ui.label('label A').mark('important')
    ui.button('button B')
    ui.label('label B').mark('normal')

    assert texts(ElementFilter(kind=TextElement).exclude(marker='normal')) == ['label A', 'button B']


def test_find_with_excluding_text():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    assert texts(ElementFilter(kind=ui.button).exclude(content='A')) == ['button B']


def test_find_not_within_kind():
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter(kind=ui.button).not_within(kind=ui.row)) == ['button A']


def test_find_not_within_marker():
    ui.button('button A')
    ui.label('label A')
    with ui.row().mark('horizontal'):
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter(kind=ui.button).not_within(marker='horizontal')) == ['button A']


def test_find_not_within_element():
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    assert texts(ElementFilter(kind=ui.button).not_within(instance=r)) == ['button A']


def test_find_in_local_scope():
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')
        assert texts(ElementFilter(local_scope=True)) == ['button B', 'label B']


def test_multiple_markers():
    ui.button('AB').mark('a b')
    ui.button('A').mark('a')

    assert texts(ElementFilter(marker='a b')) == ['AB']
    assert texts(ElementFilter(marker='b a')) == ['AB']
    assert texts(ElementFilter(marker='b')) == ['AB']
    assert texts(ElementFilter(marker='a')) == ['AB', 'A']


def test_multiple_parent_markers():
    with ui.row().mark('a b'):
        ui.label('Label 1')
    with ui.row().mark('a'):
        ui.label('Label 2')
    ui.label('Label 3')

    assert texts(ElementFilter(kind=ui.label).within(marker='a b')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='b a')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='b')) == ['Label 1']
    assert texts(ElementFilter(kind=ui.label).within(marker='a')) == ['Label 1', 'Label 2']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='a b')) == ['Label 2', 'Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='b a')) == ['Label 2', 'Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='b')) == ['Label 2', 'Label 3']
    assert texts(ElementFilter(kind=ui.label).not_within(marker='a')) == ['Label 3']


async def test_setting_classes(user: User):
    ui.label('label A')
    ui.label('label B')

    ElementFilter(kind=ui.label).classes('text-2xl')

    await user.open('/')
    for label in user.find('label').elements:
        assert label._classes == ['text-2xl']  # pylint: disable=protected-access


async def test_setting_style(user: User):
    ui.label('label A')
    ui.label('label B')

    ElementFilter(kind=ui.label).style('color: red')

    await user.open('/')
    for label in user.find('label').elements:
        assert label._style['color'] == 'red'  # pylint: disable=protected-access


async def test_setting_props(user: User):
    ui.button('button A')
    ui.button('button B')

    ElementFilter(kind=ui.button).props('flat')

    await user.open('/')
    for button in user.find('button').elements:
        assert button._props['flat']  # pylint: disable=protected-access


async def test_typing(user: User):
    ui.button('button A')
    ui.label('label A')

    await user.open('/')
    # NOTE we have not yet found a way to test the typing suggestions automatically
    # to test, hover over the variable and verify that your IDE infers the correct type
    _ = ElementFilter(kind=ui.button)  # ElementFilter[ui.button]
    _ = ElementFilter(kind=ui.label)  # ElementFilter[ui.label]
    _ = ElementFilter()  # ElementFilter[Element]
