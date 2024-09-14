from nicegui import ui

from . import doc


@doc.demo(ui.checkbox)
def main_demo() -> None:
    checkbox = ui.checkbox('check me')
    ui.label('Check!').bind_visibility_from(checkbox, 'value')


@doc.demo('Handle User Interaction', '''
    The `on_change` function passed via parameter will be called when the checkbox is clicked
    *and* when the value changes via `set_value` call.
    To execute a function only when the user interacts with the checkbox, you can use the generic `on` method.
''')
def user_interaction():
    with ui.row():
        c1 = ui.checkbox(on_change=lambda e: ui.notify(str(e.value)))
        ui.button('set value', on_click=lambda: c1.set_value(not c1.value))
    with ui.row():
        c2 = ui.checkbox().on('click', lambda e: ui.notify(str(e.sender.value)))
        ui.button('set value', on_click=lambda: c2.set_value(not c2.value))


doc.reference(ui.checkbox)
