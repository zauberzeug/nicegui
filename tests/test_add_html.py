from nicegui import ui
from nicegui.testing import Screen


def test_add_head_html(screen: Screen) -> None:
    @ui.page('/')
    def page():
        ui.add_head_html(r'<style>.my-label {background: rgb(0, 0, 255)}</style>')
        ui.label('Label').classes('my-label')
        ui.button('Green', on_click=lambda: ui.add_head_html(r'<style>.my-label {background: rgb(0, 255, 0)}</style>'))

    screen.open('/')
    assert screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'

    screen.click('Green')
    screen.wait(0.5)
    assert screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 255, 0, 1)'


def test_css(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_css('''
            .red {
                color: red;
            }
        ''')
        ui.label('This is red with CSS.').classes('red')

    screen.open('/')
    assert screen.find('This is red with CSS.').value_of_css_property('color') == 'rgba(255, 0, 0, 1)'


def test_scss(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_scss('''
            .green {
                background-color: lightgreen;
                .blue {
                    color: blue;
                }
            }
        ''')
        with ui.element().classes('green'):
            ui.label('This is blue on green with SCSS.').classes('blue')

    screen.open('/')
    assert screen.find('This is blue on green with SCSS.').value_of_css_property('color') == 'rgba(0, 0, 255, 1)'


def test_sass(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_sass('''
            .yellow
                background-color: yellow
                .purple
                    color: purple
        ''')
        with ui.element().classes('yellow'):
            ui.label('This is purple on yellow with SASS.').classes('purple')

    screen.open('/')
    assert screen.find('This is purple on yellow with SASS.').value_of_css_property('color') == 'rgba(128, 0, 128, 1)'
