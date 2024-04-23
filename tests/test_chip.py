from nicegui import ui
from nicegui.testing import Screen


def test_hello_world(screen: Screen):
    text = 'Hello, world'
    chip = ui.chip(text, removable=True)

    screen.open('/')
    screen.should_contain(text)

    chip.set_value(False)
    screen.wait(0.5)
    screen.should_not_contain(text)


def test_selectable(screen: Screen):
    text = 'Selectable'
    chip = ui.chip(text, selectable=True)
    assert not chip.selected

    screen.open('/')
    screen.should_contain(text)

    screen.click(text)
    screen.should_contain(text)
    assert chip.selected

    screen.click(text)
    screen.should_contain(text)
    assert not chip.selected
