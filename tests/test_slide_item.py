from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import SharedScreen


def test_slide_item(shared_screen: SharedScreen):
    slide_item = None

    @ui.page('/')
    def page():
        nonlocal slide_item
        label = ui.label('None')
        with ui.slide_item('slide item', on_slide=lambda e: label.set_text(f'Event: {e.side}')) as slide_item:
            slide_item.left()

    shared_screen.open('/')
    shared_screen.should_contain('slide item')
    shared_screen.should_contain('None')

    ActionChains(shared_screen.selenium) \
        .move_to_element_with_offset(shared_screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    shared_screen.should_contain('Event: left')


def test_slide_side(shared_screen: SharedScreen):
    slide_item = None

    @ui.page('/')
    def page():
        nonlocal slide_item
        label = ui.label('None')
        with ui.slide_item('slide item') as slide_item:
            slide_item.left(on_slide=lambda e: label.set_text(f'Event: {e.side}'))
            slide_item.right(on_slide=lambda e: label.set_text(f'Event: {e.side}'))

    shared_screen.open('/')
    shared_screen.should_contain('None')

    ActionChains(shared_screen.selenium) \
        .move_to_element_with_offset(shared_screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    shared_screen.should_contain('Event: left')

    slide_item.reset()
    shared_screen.should_contain('slide item')

    ActionChains(shared_screen.selenium) \
        .move_to_element_with_offset(shared_screen.find_element(slide_item), 20, 0) \
        .click_and_hold() \
        .pause(0.5) \
        .move_by_offset(-60, 0) \
        .pause(0.5) \
        .release() \
        .perform()
    shared_screen.should_contain('Event: right')
