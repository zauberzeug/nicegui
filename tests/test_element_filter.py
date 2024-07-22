from typing import List

import pytest

from nicegui import ElementFilter, ui
from nicegui.elements.mixins.text_element import TextElement
from nicegui.testing import User

pytestmark = pytest.mark.usefixtures('user')

# pylint: disable=missing-function-docstring


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

    result = [element.text for element in ElementFilter(kind=TextElement)]

    assert result == ['button A', 'label A', 'button B', 'label B']


def test_find_by_kind():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [element.text for element in ElementFilter(kind=ui.button)]

    assert result == ['button A', 'button B']


def test_find_by_containing_text():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [element.text for element in ElementFilter(content='A')]

    assert result == ['button A', 'label A']


def test_find_by_containing_texts():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [element.text for element in ElementFilter(content=['A', 'tt'])]

    assert result == ['button A']


def test_find_by_marker():
    ui.button('button A')
    ui.button('button B').mark('important')

    result = [element.text for element in ElementFilter(marker='important')]

    assert result == ['button B']


def test_find_by_specific_marker():
    ui.button('button A').mark('test')
    ui.button('button B').mark('important ', 'test')
    ui.button('button C').mark(' important test')

    test = [element.text for element in ElementFilter(marker='test')]
    important = [element.text for element in ElementFilter(marker='important')]

    assert test == ['button A', 'button B', 'button C']
    assert important == ['button B', 'button C']


def test_find_by_multiple_markers():
    ui.button('button A').mark('test')
    ui.button('button B').mark('important ', 'test')
    ui.button('button C').mark(' important test')

    search = ElementFilter(kind=ui.button, marker='test important')
    result = [element.text for element in search]

    assert result == ['button B', 'button C']


def test_find_within_marker():
    ui.button('button A')
    ui.label('label A')
    with ui.row().mark('horizontal'):
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter().within(marker='horizontal')]

    assert result == ['button B', 'label B']


def test_find_within_element():
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter().within(instance=r)]

    assert result == ['button B', 'label B']


def test_find_within_elements():
    with ui.row() as row1:
        ui.button('button A')
        ui.label('label A')
    with ui.row() as row2:
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter().within(instance=[row1, row2])]

    assert result == ['button A', 'label A', 'button B', 'label B']


def test_find_within_kind():
    ui.button('button A')
    with ui.row():
        ui.label('label A')
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter(content='B').within(kind=ui.row)]

    assert result == ['button B', 'label B']


def test_find_with_excluding_kind():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [element.text for element in ElementFilter(content='A').exclude(kind=ui.label)]

    assert result == ['button A']


def test_find_with_excluding_marker():
    ui.button('button A').mark('normal')
    ui.label('label A').mark('important')
    ui.button('button B')
    ui.label('label B').mark('normal')

    result = [element.text for element in ElementFilter(kind=TextElement).exclude(marker='normal')]

    assert result == ['label A', 'button B']


def test_find_with_excluding_text():
    ui.button('button A')
    ui.label('label A')
    ui.button('button B')
    ui.label('label B')

    result = [element.text for element in ElementFilter(kind=ui.button).exclude(content='A')]

    assert result == ['button B']


def test_find_not_within_kind():
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter(kind=ui.button).not_within(kind=ui.row)]

    assert result == ['button A']


def test_find_not_within_marker():
    ui.button('button A')
    ui.label('label A')
    with ui.row().mark('horizontal'):
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter(kind=ui.button).not_within(marker='horizontal')]

    assert result == ['button A']


def test_find_not_within_element():
    ui.button('button A')
    ui.label('label A')
    with ui.row() as r:
        ui.button('button B')
        ui.label('label B')

    result = [element.text for element in ElementFilter(kind=ui.button).not_within(instance=r)]

    assert result == ['button A']


def test_find_in_local_scope():
    ui.button('button A')
    ui.label('label A')
    with ui.row():
        ui.button('button B')
        ui.label('label B')
        result = [element.text for element in ElementFilter(local_scope=True)]

    assert result == ['button B', 'label B']


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
    # to test, hover over the variable and verify that your IDE inferres the correct type
    _ = ElementFilter(kind=ui.button)  # ElementFilter[ui.button]
    _ = ElementFilter(kind=ui.label)  # ElementFilter[ui.label]
    _ = ElementFilter()  # ElementFilter[Element]
