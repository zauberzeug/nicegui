from nicegui import ui
from nicegui.testing import Screen


def test_pagination(screen: Screen):
    p = ui.pagination(1, 10, direction_links=True)
    ui.label().bind_text_from(p, 'value', lambda v: f'Page {v}')

    screen.open('/')
    screen.should_contain('Page 1')

    screen.click('7')
    screen.should_contain('Page 7')

    screen.click('keyboard_arrow_left')
    screen.should_contain('Page 6')

    screen.click('keyboard_arrow_right')
    screen.should_contain('Page 7')
