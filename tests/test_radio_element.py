from nicegui import events, ui
from nicegui.testing import Screen

def test_radio_click(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    screen.click('A')
    assert r.value == 'A'
    screen.click('B')
    assert r.value == 'B'

def test_radio_click_already_selected(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='B')

    screen.open('/')
    screen.click('B')
    assert r.value == 'B'

def test_radio_set_value(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_value('B')
    assert r.value == 'B'

def test_radio_set_options(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_options(['D', 'E', 'F'])
    assert r.options == ['D', 'E', 'F']

def test_radio_set_options_value_still_valid(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='C')

    screen.open('/')
    r.set_options(['C', 'D', 'E'])
    assert r.value == 'C'

def test_radio_set_options_value_none(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='C')

    screen.open('/')
    r.set_options(['D', 'E', 'F'])
    assert r.value is None

def test_radio_set_options_value(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_options(['D', 'E', 'F'], value='E')
    assert r.value == 'E'

def test_radio_set_options_value_callback(screen: Screen):
    """Fix for https://github.com/zauberzeug/nicegui/issues/3733.

    When using `set_options` with the value argument set and the `on_change` callback active on the element,
    `on_change` should never pass `None` through, even if the old value is not within the new list of element options.
    """

    def check_change_is_not_none(e: events.ValueChangeEventArguments):
        assert e.value is not None

    r = ui.radio(['A', 'B', 'C'], on_change=check_change_is_not_none)

    screen.open('/')
    r.set_options(['D', 'E', 'F'], value='F')
