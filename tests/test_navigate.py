import pytest

from nicegui import ui
from nicegui.testing import SharedScreen


@pytest.mark.parametrize('new_tab', [False, True])
def test_navigate_to(shared_screen: SharedScreen, new_tab: bool):
    @ui.page('/test_page')
    def test_page():
        ui.label('Test page')
        ui.button('Back', on_click=ui.navigate.back)

    @ui.page('/')
    def page():
        ui.button('Open test page', on_click=lambda: ui.navigate.to('/test_page', new_tab=new_tab))
        ui.button('Forward', on_click=ui.navigate.forward)

    shared_screen.open('/')
    shared_screen.click('Open test page')
    shared_screen.wait(0.5)
    shared_screen.switch_to(1 if new_tab else 0)
    shared_screen.should_contain('Test page')

    if not new_tab:
        shared_screen.click('Back')
        shared_screen.should_contain('Open test page')

        shared_screen.click('Forward')
        shared_screen.should_contain('Test page')


def test_navigate_to_absolute_url(shared_screen: SharedScreen):
    external_url = 'https://www.google.com/'

    @ui.page('/')
    def page():
        ui.button('Go external', on_click=lambda: ui.navigate.to(external_url))

    shared_screen.open('/')
    shared_screen.click('Go external')
    shared_screen.wait(1.0)
    assert external_url in shared_screen.selenium.current_url


def test_navigate_to_relative_url(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Index page')
        ui.button('Go test page', on_click=lambda: ui.navigate.to('/test_page'))

    @ui.page('/test_page')
    def test_page():
        ui.label('Test page')
        ui.button('Back', on_click=ui.navigate.back)

    shared_screen.open('/')
    shared_screen.click('Go test page')
    shared_screen.should_contain('Test page')

    shared_screen.click('Back')
    shared_screen.should_contain('Index page')


@pytest.mark.parametrize('sub_pages', [False, True])
def test_navigate_to_mailto_url(shared_screen: SharedScreen, sub_pages: bool):
    @ui.page('/')
    def page():
        ui.button('Send mail', on_click=lambda: ui.navigate.to('mailto:test@example.com'))
        if sub_pages:
            ui.sub_pages({'/': lambda: ui.label('sub page')})

    shared_screen.open('/')
    # Override window.open to capture calls instead of triggering the system mail client
    shared_screen.selenium.execute_script('window.__open_calls = [];'
                                   'window.open = (url, target) => window.__open_calls.push([url, target]);')
    shared_screen.click('Send mail')
    shared_screen.wait(0.5)
    assert shared_screen.selenium.execute_script('return window.__open_calls') == [['mailto:test@example.com', '_self']]


def test_xss_via_history_push(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.button('Push', on_click=lambda: ui.navigate.history.push('/");console.log("XSS");//'))

    shared_screen.open('/')
    shared_screen.click('Push')
    shared_screen.wait(1)
    assert 'XSS' not in shared_screen.render_js_logs()
