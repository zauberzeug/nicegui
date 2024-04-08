import pytest

from nicegui import ui, app, context
from nicegui.testing import Screen


def test_session_state(screen: Screen):
    def increment():
        app.storage.client['counter'] = app.storage.client['counter'] + 1

    @ui.page('/')
    async def page():
        app.storage.client['counter'] = 123
        ui.button('Increment').on_click(increment)
        ui.label().bind_text(app.storage.client, 'counter')
        ui.button('Increment').on_click(increment)
        ui.label().bind_text(app.storage.client, 'counter')

    screen.open('/')
    screen.should_contain('123')
    screen.click('Increment')
    screen.wait_for('124')
    screen.switch_to(1)
    screen.open('/')
    screen.should_contain('123')
    screen.switch_to(0)
    screen.should_contain('124')

def test_clear(screen: Screen):
    with pytest.raises(RuntimeError):  # no context (auto index)
        app.storage.client.clear()

    @ui.page('/')
    async def page():
        await context.get_client().connected()
        app.storage.client['counter'] = 123
        app.storage.client.clear()
        assert 'counter' not in app.storage.client

    screen.open('/')
