from nicegui import ui

from . import doc


@doc.demo(ui.popup)
def main_demo() -> None:
    from nicegui import app

    app.storage.client['name'] = 'NiceGUI User'

    with ui.label().bind_text_from(app.storage.client, 'name'):
        with ui.popup() as popup:
            ui.input().props('autofocus') \
                .bind_value(app.storage.client, 'name') \
                .on('keydown.enter', popup.close)


doc.reference(ui.popup)
