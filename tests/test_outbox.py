import asyncio

from nicegui import app, ui
from nicegui.testing import Screen


def test_removing_outbox_loops(screen: Screen):
    @ui.page('/')
    def page():
        ui.label('Index page')

    @ui.page('/subpage', reconnect_timeout=0.1)
    def subpage():
        ui.button('Click me', on_click=lambda: ui.notify('Hello world!'))

    state = {'count': 0}
    app.timer(0.1, lambda: state.update(count=len([t for t in asyncio.all_tasks()
                                                   if t.get_name().startswith('outbox loop')])))

    screen.open('/subpage')
    screen.click('Click me')
    screen.should_contain('Hello world!')
    assert state['count'] == 1

    screen.open('/')
    screen.should_contain('Index page')
    screen.wait(0.5)  # wait for the outbox loop to finish
    assert state['count'] == 1
