from nicegui import ui, app
from nicegui.testing import Screen


def test_session_state(screen: Screen):
    app.storage.client['counter'] = 123

    def increment():
        app.storage.client['counter'] = app.storage.client['counter'] + 1

    ui.button('Increment').on_click(increment)
    ui.label().bind_text(app.storage.client, 'counter')

    screen.open('/')
    screen.should_contain('123')
    screen.click('Increment')
    screen.wait_for('124')


def test_clear(screen: Screen):
    app.storage.client['counter'] = 123
    app.storage.client.clear()
    assert 'counter' not in app.storage.client
