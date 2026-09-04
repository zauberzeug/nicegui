from nicegui import app, ui
from nicegui.testing import Screen


def test_appwide_colors(screen: Screen):
    app.colors(primary='#ff0000', brand='#00ff00')

    @ui.page('/')
    def page():
        ui.button('Test Button')
        ui.button('Brand Button', color='brand')

    screen.open('/')
    assert screen.find_all_by_tag('button')[0].value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
    assert screen.find_all_by_tag('button')[1].value_of_css_property('background-color') == 'rgba(0, 255, 0, 1)'


def test_replace_colors(screen: Screen):
    @ui.page('/')
    def page():
        with ui.row() as container:
            ui.colors(primary='blue')

        def replace():
            with container.clear():
                ui.colors(primary='red')
        ui.button('Replace', on_click=replace)

    screen.open('/')
    assert screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'

    screen.click('Replace')
    screen.wait(0.5)
    assert screen.find_by_tag('button').value_of_css_property('background-color') == 'rgba(255, 0, 0, 1)'
