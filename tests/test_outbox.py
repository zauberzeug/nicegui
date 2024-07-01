import asyncio

from nicegui import ui
from nicegui.testing import SeleniumScreen


def test_removing_outbox_loops(screen: SeleniumScreen):
    @ui.page('/page', reconnect_timeout=0.1)
    def page():
        ui.button('Click me', on_click=lambda: ui.notify('Hello world!'))

    def count_outbox_loop_tasks() -> int:
        return len([t for t in asyncio.all_tasks() if t.get_name().startswith('outbox loop')])

    count = ui.label()
    ui.timer(0.1, lambda: count.set_text(f'{count_outbox_loop_tasks()} tasks'))

    screen.open('/page')
    screen.click('Click me')
    screen.should_contain('Hello world!')
    assert count.text == '1 tasks'

    screen.open('/')
    screen.wait(0.5)
    assert count.text == '0 tasks'
