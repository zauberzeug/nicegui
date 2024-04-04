from nicegui import ui, app
from nicegui.testing import Screen


def test_session_state(screen: Screen):
    app.storage.session["counter"] = 123

    def increment():
        app.storage.session["counter"] = app.storage.session["counter"] + 1

    ui.button("Increment").on_click(increment)
    ui.label().bind_text(app.storage.session, "counter")

    screen.open('/')
    screen.should_contain('123')
    screen.click('Increment')
    screen.wait_for('124')
