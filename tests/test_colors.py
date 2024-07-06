from nicegui import ui
from nicegui.testing import Screen


def test_replace_colors(screen: Screen):
    with ui.row() as container:
        ui.colors(primary='blue')

    def replace():
        container.clear()
        with container:
            ui.colors(primary='red')
    ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'
    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
