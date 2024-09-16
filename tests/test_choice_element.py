from nicegui import ui
from nicegui.testing import Screen


###

# Tests Needed:

# - Radio options should be clickable, and the value should be set to the clicked option

def test_radio_click(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    screen.click('A')
    assert r.value == 'A'
    screen.click('B')
    assert r.value == 'B'

# - Clicking an option that is already selectable should do nothing

def test_radio_click_already_selected(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='B')

    screen.open('/')
    screen.click('B')
    assert r.value == 'B'

# - Element value should be settable by invoking `set_value`

def test_radio_set_value(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_value('B')
    assert r.value == 'B'

# - Element options should be settable by invoking `set_options`

def test_radio_set_options(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_options(['D', 'E', 'F'])
    assert r.options == ['D', 'E', 'F']

# - When using `set_options`, the new value should still be what the old value was if the old value is within the new list of element options

def test_radio_set_options_value_still_valid(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='C')

    screen.open('/')
    r.set_options(['C', 'D', 'E'])
    assert r.value == 'C'

# - When using `set_options`, the new value should be set to `None` if the old value is not within the new list of element options

def test_radio_set_options_value_none(screen: Screen):
    r = ui.radio(['A', 'B', 'C'], value='C')

    screen.open('/')
    r.set_options(['D', 'E', 'F'])
    assert r.value is None

# - When using `set_options` with the value argument set, the new value should be properly set

def test_radio_set_options_value(screen: Screen):
    r = ui.radio(['A', 'B', 'C'])

    screen.open('/')
    r.set_options(['D', 'E', 'F'], value='E')
    assert r.value == 'E'

###
