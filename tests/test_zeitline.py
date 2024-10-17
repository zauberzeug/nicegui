from nicegui import ui
from nicegui.testing import Screen


def test_zeitline(screen: Screen):

    t = ui.zeitline()
    t.add_event('2017-01-01', 'new!')
    ui.button('add', on_click=lambda: t.add_event('2028-01-02', 'renew!'))

    screen.open('/')
    screen.should_not_contain('renew!')
    screen.click('add')
    screen.should_contain('new!')
    screen.should_contain('renew!')


