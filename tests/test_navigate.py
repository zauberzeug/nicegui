import pytest

from nicegui import ui
from nicegui.testing import Screen


@pytest.mark.parametrize('new_tab', [False, True])
def test_navigate_to(screen: Screen, new_tab: bool):
    @ui.page('/test_page')
    def test_page():
        ui.label('Test page')
        ui.button('Back', on_click=ui.navigate.back)

    @ui.page('/')
    def page():
        ui.button('Open test page', on_click=lambda: ui.navigate.to('/test_page', new_tab=new_tab))
        ui.button('Forward', on_click=ui.navigate.forward)

    screen.open('/')
    screen.click('Open test page')
    screen.wait(0.5)
    screen.switch_to(1 if new_tab else 0)
    screen.should_contain('Test page')

    if not new_tab:
        screen.click('Back')
        screen.should_contain('Open test page')

        screen.click('Forward')
        screen.should_contain('Test page')


def test_navigate_to_absolute_url(screen: Screen):
    external_url = 'https://www.google.com/'

    @ui.page('/')
    def page():
        ui.button('Go external', on_click=lambda: ui.navigate.to(external_url))

    screen.open('/')
    screen.click('Go external')
    screen.wait(1.0)
    assert external_url in screen.selenium.current_url


def test_navigate_to_relative_url(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Index page')
        ui.button('Go test page', on_click=lambda: ui.navigate.to('/test_page'))

    @ui.page('/test_page')
    def test_page():
        ui.label('Test page')
        ui.button('Back', on_click=ui.navigate.back)

    screen.open('/')
    screen.click('Go test page')
    screen.should_contain('Test page')

    screen.click('Back')
    screen.should_contain('Index page')


@pytest.mark.parametrize('sub_pages', [False, True])
def test_navigate_to_mailto_url(screen: Screen, sub_pages: bool):
    @ui.page('/')
    def page():
        ui.button('Send mail', on_click=lambda: ui.navigate.to('mailto:test@example.com'))
        if sub_pages:
            ui.sub_pages({'/': lambda: ui.label('sub page')})

    screen.open('/')
    # Override window.open to capture calls instead of triggering the system mail client
    screen.selenium.execute_script('window.__open_calls = [];'
                                   'window.open = (url, target) => window.__open_calls.push([url, target]);')
    screen.click('Send mail')
    screen.wait(0.5)
    assert screen.selenium.execute_script('return window.__open_calls') == [['mailto:test@example.com', '_self']]
