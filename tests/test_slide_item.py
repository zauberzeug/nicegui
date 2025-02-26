from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_slide_item(screen: Screen):
    with ui.slide_item(on_change=lambda: label.set_text('Event: change')) as s:
        ui.label('slide item')
        s.slide(side='left')
    label = ui.label('None')

    screen.open('/')
    slide_item = screen.find_element(s)
    screen.should_contain('slide item')
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(slide_item, -20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.wait(1)
    screen.should_contain('Event: change')


def test_slide_side(screen: Screen):
    with ui.slide_item() as s:
        ui.label('slide item')
        s.slide(side='left', on_slide=lambda: label.set_text('Event: left slide'))
        s.slide(side='right', on_slide=lambda: label.set_text('Event: right slide'))

    label = ui.label('None')

    screen.open('/')
    slide_item = screen.find_element(s)
    screen.should_contain('None')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(slide_item, -20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.wait(1)
    screen.should_contain('Event: left slide')

    s.reset()
    screen.wait(1)

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(slide_item, 20, 0) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(-60, 0) \
        .pause(1) \
        .release() \
        .perform()
    screen.wait(1)
    screen.should_contain('Event: right slide')
