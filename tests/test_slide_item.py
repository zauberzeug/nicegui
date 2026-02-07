from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen
import pytest



@pytest.fixture(autouse=True)
def enable_csp_for_module(enable_csp):
    """Enable CSP for all tests in this module to verify CSP compatibility."""
    yield




def test_slide_item(screen: Screen):
    slide_item = None

    @ui.page('/')
    def page():
        nonlocal slide_item
        label = ui.label('None')
        with ui.slide_item('slide item', on_slide=lambda e: label.set_text(f'Event: {e.side}')) as slide_item:
            slide_item.left()

    screen.open('/')
    screen.should_contain('slide item')
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    screen.should_contain('Event: left')


def test_slide_side(screen: Screen):
    slide_item = None

    @ui.page('/')
    def page():
        nonlocal slide_item
        label = ui.label('None')
        with ui.slide_item('slide item') as slide_item:
            slide_item.left(on_slide=lambda e: label.set_text(f'Event: {e.side}'))
            slide_item.right(on_slide=lambda e: label.set_text(f'Event: {e.side}'))

    screen.open('/')
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    screen.should_contain('Event: left')

    slide_item.reset()
    screen.should_contain('slide item')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), 20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(-60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    screen.should_contain('Event: right')
