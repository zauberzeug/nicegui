from itertools import pairwise

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from nicegui import ui
from nicegui.testing import Screen


def _is_in_viewport(screen: Screen, element: WebElement) -> bool:
    return screen.selenium.execute_script('''
        const rect = arguments[0].getBoundingClientRect();
        return rect.top >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.left >= 0 && rect.right <= (window.innerWidth || document.documentElement.clientWidth);
    ''', element)


def _assert_dom_order(screen: Screen, *elements: WebElement) -> None:
    for first, second in pairwise(elements):
        assert screen.selenium.execute_script('''
            return arguments[0].compareDocumentPosition(arguments[1]) & Node.DOCUMENT_POSITION_FOLLOWING;
        ''', first, second)


def test_skip_link_skips_to_offscreen_content(screen: Screen):
    @ui.page('/')
    def page():
        with ui.column().style('height: 200vh'):
            ui.button('Navigation')
        ui.skip_link(target=ui.label('Main content'))

    screen.open('/')
    screen.should_contain('Navigation')
    screen.should_contain('Skip to main content')  # invisible, but present in the DOM
    assert not _is_in_viewport(screen, screen.find('Main content'))

    screen.type(Keys.TAB)
    screen.type(Keys.ENTER)
    assert _is_in_viewport(screen, screen.find('Main content'))


def test_skip_link_with_custom_text(screen: Screen):
    @ui.page('/')
    def page():
        ui.skip_link('Skip navigation', target=ui.label('Main content'))

    screen.open('/')
    screen.should_contain('Skip navigation')


def test_skip_link_with_context_manager_replaces_text(screen: Screen):
    @ui.page('/')
    def page():
        with ui.skip_link(text='', target=ui.label('Main content')):
            ui.label('Jump to content')

    screen.open('/')
    screen.should_contain('Jump to content')
    screen.should_not_contain('Skip to main content')


def test_skip_link_order(screen: Screen):
    @ui.page('/')
    def page():
        ui.button('Navigation')
        ui.skip_link('Skip link A', target=ui.label('Content A'))
        ui.skip_link('Skip link B', target=ui.label('Content B'))

    screen.open('/')
    _assert_dom_order(screen, screen.find('Skip link A'), screen.find('Skip link B'), screen.find('Navigation'))


def test_link_is_deleted_with_calling_context(screen: Screen):
    link = None

    @ui.page('/')
    def page():
        nonlocal link
        with ui.column() as container:
            link = ui.skip_link(target=ui.label('Main content'))
        ui.button('Clear', on_click=container.clear)

    screen.open('/')
    screen.click('Clear')
    screen.wait_for(lambda: link.is_deleted)
