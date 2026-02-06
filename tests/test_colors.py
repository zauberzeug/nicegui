from nicegui import app, ui
from nicegui.testing import SharedScreen


def test_appwide_colors(shared_screen: SharedScreen):
    app.colors(primary='#ff0000', brand='#00ff00')

    @ui.page('/')
    def page():
        ui.button('Test Button')
        ui.button('Brand Button', color='brand')

    shared_screen.open('/')
    assert shared_screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
    assert shared_screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 255, 0, 1)'


def test_replace_colors(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.colors(primary='blue')

        def replace():
            with container.clear():
                ui.colors(primary='red')
        ui.button('Replace', on_click=replace)

    shared_screen.open('/')
    assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'

    shared_screen.click('Replace')
    shared_screen.wait(0.5)
    assert shared_screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
