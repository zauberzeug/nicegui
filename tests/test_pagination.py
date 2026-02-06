from nicegui import ui
from nicegui.testing import SharedScreen


def test_pagination(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        p = ui.pagination(1, 10, direction_links=True)
        ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')

    shared_screen.open('/')
    shared_screen.should_contain('Page 1')

    shared_screen.click('7')
    shared_screen.should_contain('Page 7')

    shared_screen.click('keyboard_arrow_left')
    shared_screen.should_contain('Page 6')

    shared_screen.click('keyboard_arrow_right')
    shared_screen.should_contain('Page 7')
