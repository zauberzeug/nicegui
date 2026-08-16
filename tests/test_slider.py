from selenium.webdriver.common.action_chains import ActionChains

from nicegui import ui
from nicegui.testing import Screen


def test_slider_on_release_waits_for_the_release(screen: Screen):
    s = None

    @ui.page('/')
    def page():
        nonlocal s
        s = ui.slider(min=0, max=100, value=50,
                      on_change=lambda e: changed.set_text(f'changed {e.value}'),
                      on_release=lambda e: released.set_text(f'released {e.value}'))
        changed = ui.label('changed -')
        released = ui.label('released -')

    screen.open('/')
    slider = screen.find_element(s)

    ActionChains(screen.selenium) \
        .move_to_element(slider) \
        .click_and_hold() \
        .move_by_offset(40, 0) \
        .pause(0.5) \
        .perform()
    screen.should_not_contain('changed -')  # on_change fires while dragging
    screen.should_contain('released -')  # on_release does not

    ActionChains(screen.selenium).release().perform()
    screen.should_not_contain('released -')
    screen.should_contain(f'released {s.value}')
