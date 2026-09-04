from nicegui import ui

from . import doc


@doc.demo(ui.switch)
def main_demo() -> None:
    switch = ui.switch('switch me')
    ui.label('Switch!').bind_visibility_from(switch, 'value')


@doc.demo('Handle User Interaction', '''
    The `on_change` function passed via parameter will be called when the switch is clicked
    *and* when the value changes via `set_value` call.
    To execute a function only when the user interacts with the switch, you can use the generic `on` method.
''')
def user_interaction():
    with ui.row():
        s1 = ui.switch(on_change=lambda e: ui.notify(str(e.value)))
        ui.button('set value', on_click=lambda: s1.set_value(not s1.value))
    with ui.row():
        s2 = ui.switch().on('click', lambda e: ui.notify(str(e.sender.value)))
        ui.button('set value', on_click=lambda: s2.set_value(not s2.value))


doc.reference(ui.switch)
