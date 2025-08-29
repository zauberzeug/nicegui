from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_joystick(screen: Screen):
    j = None

    @ui.page('/')
    def page():
        nonlocal j
        j = ui.joystick(on_move=lambda e: coordinates.set_text(f'move {e.x:.3f}, {e.y:.3f}'),
                        on_end=lambda _: coordinates.set_text('end 0, 0'))
        coordinates = ui.label('start 0, 0')

    screen.open('/')
    joystick = screen.find_element(j)
    assert joystick
    screen.should_contain('start 0, 0')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(joystick, 25, 25) \
        .click_and_hold() \
        .pause(1) \
        .move_by_offset(20, 20) \
        .pause(1) \
        .perform()
    screen.should_contain('move 0.400, -0.400')

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(joystick, 25, 25) \
        .click() \
        .perform()
    screen.should_contain('end 0, 0')


def test_styling_joystick(screen: Screen):
    j = None

    @ui.page('/')
    def page():
        nonlocal j
        j = ui.joystick().style('background-color: gray;').classes('shadow-lg')

    screen.open('/')
    joystick = screen.find_element(j)
    assert 'background-color: gray;' in joystick.get_attribute('style')
    assert 'shadow-lg' in joystick.get_attribute('class')
