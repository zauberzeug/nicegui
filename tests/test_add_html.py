import asyncio

import pytest

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


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_css(screen: Screen, shared: bool, delayed: bool):
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

    screen.open('/')
    label = screen.find('This is red with CSS.')
    screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(255, 0, 0, 1)'


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_scss(screen: Screen, shared: bool, delayed: bool):
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

    screen.open('/')
    label = screen.find('This is blue on green with SCSS.')
    screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(0, 0, 255, 1)'


@pytest.mark.parametrize('shared', [False, True])
@pytest.mark.parametrize('delayed', [False, True])
def test_sass(screen: Screen, shared: bool, delayed: bool):
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

    screen.open('/')
    label = screen.find('This is purple on yellow with SASS.')
    screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(128, 0, 128, 1)'


def test_add_body_html_after_await_in_async_sub_page(screen: Screen):
    """add_body_html must survive a page load when called after an await in an async sub page builder,
    without being injected twice on a normal load (#6147)."""
    async def sub():
        await asyncio.sleep(0)  # resumes after the response is built, before the socket connects
        ui.add_body_html('<div id="injected-marker">injected</div>')

    @ui.page('/')
    def index():
        ui.sub_pages({'/': sub})

    screen.open('/')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return document.querySelectorAll("#injected-marker").length') == 1


def test_add_css_after_await_in_async_sub_page(screen: Screen):
    """add_css must survive a page load when called after an await in an async sub page builder (#6147)."""
    async def sub():
        await asyncio.sleep(0)  # resumes after the response is built, before the socket connects
        ui.add_css('.late { color: rgb(255, 0, 0); }')
        ui.label('late css').classes('late')

    @ui.page('/')
    def index():
        ui.sub_pages({'/': sub})

    screen.open('/')
    label = screen.find('late css')
    screen.wait(0.5)
    assert label.value_of_css_property('color') == 'rgba(255, 0, 0, 1)'


def test_add_css_with_script(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_css("</style></script><script>document.write('XSS');</script>")
        ui.label('Hello, World!')

    screen.open('/')
    screen.should_contain('Hello, World!')
    screen.should_not_contain('XSS')


def test_add_scss_with_script(screen: Screen):
    @ui.page('/')
    def page():
        ui.add_scss("</style></script><script>document.write('XSS');</script>")
        ui.label('Hello, World!')

    screen.allowed_js_errors.append('static/sass.dart.js')
    screen.open('/')
    screen.should_contain('Hello, World!')
    screen.should_not_contain('XSS')
