from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_slide_item(screen: Screen):
    with ui.slide_item(on_change=lambda: label.set_text('Event: change')) as slide_item:
        ui.label('slide item')
        slide_item.slide(side='left')
    label = ui.label('None')

    screen.open('/')
    screen.should_contain('slide item')
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.should_contain('Event: change')


def test_slide_side(screen: Screen):
    with ui.slide_item() as slide_item:
        ui.label('slide item')
        slide_item.slide(side='left', on_slide=lambda: label.set_text('Event: left slide'))
        slide_item.slide(side='right', on_slide=lambda: label.set_text('Event: right slide'))

    label = ui.label('None')

    screen.open('/')
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), -20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.should_contain('Event: left slide')

    slide_item.reset()
    screen.wait(1)

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(screen.find_element(slide_item), 20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(-60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.should_contain('Event: right slide')
