import pytest

from nicegui import ui
from nicegui.testing import SharedScreen


def test_add_head_html(shared_screen: SharedScreen) -> None:
    @ui.page('/')
    def page():
        ui.add_head_html(r'<style>.my-label {background: rgb(0, 0, 255)}</style>')
        ui.label('Label').classes('my-label')
        ui.button('Green', on_click=lambda: ui.add_head_html(r'<style>.my-label {background: rgb(0, 255, 0)}</style>'))

    shared_screen.open('/')
    assert shared_screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 0, 255, 1)'

    shared_screen.click('Green')
    shared_screen.wait(0.5)
    assert shared_screen.find('Label').value_of_css_property('background-color') == 'rgba(0, 255, 0, 1)'


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_css(shared_screen: SharedScreen, shared: bool, delayed: bool):
    @ui.page('/')
    async def page():
        if delayed:
            await ui.context.client.connected()
        ui.add_css('''
            .red {
                color: red;
            }
        ''', shared=shared)
        ui.label('This is red with CSS.').classes('red')

    shared_screen.open('/')
    label = shared_screen.find('This is red with CSS.')
    shared_screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(255, 0, 0, 1)'


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_scss(shared_screen: SharedScreen, shared: bool, delayed: bool):
    @ui.page('/')
    async def page():
        if delayed:
            await ui.context.client.connected()
        ui.add_scss('''
            .green {
                background-color: lightgreen;
                .blue {
                    color: blue;
                }
            }
        ''', shared=shared)
        with ui.element().classes('green'):
            ui.label('This is blue on green with SCSS.').classes('blue')

    shared_screen.open('/')
    label = shared_screen.find('This is blue on green with SCSS.')
    shared_screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(0, 0, 255, 1)'


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_sass(shared_screen: SharedScreen, shared: bool, delayed: bool):
    @ui.page('/')
    async def page():
        if delayed:
            await ui.context.client.connected()
        ui.add_sass('''
            .yellow
                background-color: yellow
                .purple
                    color: purple
        ''', shared=shared)
        with ui.element().classes('yellow'):
            ui.label('This is purple on yellow with SASS.').classes('purple')

    shared_screen.open('/')
    label = shared_screen.find('This is purple on yellow with SASS.')
    shared_screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(128, 0, 128, 1)'


def test_add_css_with_script(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.add_css("</style></script><script>document.write('XSS');</script>")
        ui.label('Hello, World!')

    shared_screen.open('/')
    shared_screen.should_contain('Hello, World!')
    shared_screen.should_not_contain('XSS')


def test_add_scss_with_script(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.add_scss("</style></script><script>document.write('XSS');</script>")
        ui.label('Hello, World!')

    shared_screen.allowed_js_errors.append('static/sass.dart.js')
    shared_screen.open('/')
    shared_screen.should_contain('Hello, World!')
    shared_screen.should_not_contain('XSS')
