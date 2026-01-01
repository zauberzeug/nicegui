from nicegui import app, ui

from . import doc


@doc.demo(ui.popup_edit)
def main_demo() -> None:
    # from nicegui import app, ui
    app.storage.client['name'] = 'NiceGUI User'

    with ui.label().bind_text_from(app.storage.client, 'name'):
        with ui.popup_edit(on_show=lambda _: ui.notify('Shown!'),
                           on_hide=lambda _: ui.notify('Hidden!')) as popup:
            ui.input().bind_value(app.storage.client, 'name')
    ui.button('Force show popup edit', on_click=popup.show)


doc.reference(ui.popup_edit)
