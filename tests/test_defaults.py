from nicegui import ui


def test_default_props():
    assert ui.button().props['color'] == 'primary', 'primary is the default color'

    ui.button.default_props('color=red')

    assert ui.button().props['color'] == 'red', 'default props are set'
    assert ui.button(color='blue').props['color'] == 'blue', 'default props are overridden'
    assert ui.button(color='primary').props['color'] == 'primary', 'even the default color can override default props'
