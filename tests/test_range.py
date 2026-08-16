from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_range(screen: Screen):
    @ui.page('/')
    def page():
        r = ui.range(min=0, max=100, value={'min': 20, 'max': 80})
        ui.label().bind_text_from(r, 'value', backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

    screen.open('/')
    screen.should_contain('min: 20, max: 80')


def test_range_no_value(screen: Screen):
    @ui.page('/')
    def page():
        r = ui.range(min=0, max=100)
        ui.label().bind_text_from(r, 'value', backward=lambda v: f'min: {v["min"]}, max: {v["max"]}')

    screen.open('/')
    screen.should_contain('min: 0, max: 100')


def test_range_on_release_waits_for_the_release(screen: Screen):
    r = None

    @ui.page('/')
    def page():
        nonlocal r
        r = ui.range(min=0, max=100, value={'min': 20, 'max': 80},
                     on_change=lambda e: changed.set_text(f'changed {e.value["max"]}'),
                     on_release=lambda e: released.set_text(f'released {e.value["max"]}'))
        changed = ui.label('changed -')
        released = ui.label('released -')

    screen.open('/')
    range_ = screen.find_element(r)

    ActionChains(screen.selenium) \
        .move_to_element_with_offset(range_, range_.size['width'] * 3 // 10, 0) \
        .click_and_hold() \
        .move_by_offset(30, 0) \
        .pause(0.5) \
        .perform()
    screen.should_not_contain('changed -')  # on_change fires while dragging
    screen.should_contain('released -')  # on_release does not

    ActionChains(screen.selenium).release().perform()
    screen.should_not_contain('released -')
    screen.should_contain(f'released {r.value["max"]}')
