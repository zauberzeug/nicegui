from nicegui import ui

from . import doc


@doc.demo(ui.keyboard)
def main_demo() -> None:
    from nicegui.events import KeyEventArguments

    def handle_key(e: KeyEventArguments):
        if e.key == 'f' and not e.action.repeat:
            if e.action.keyup:
                ui.notify('f was just released')
            elif e.action.keydown:
                ui.notify('f was just pressed')
        if e.modifiers.shift and e.action.keydown:
            if e.key.arrow_left:
                ui.notify('going left')
            elif e.key.arrow_right:
                ui.notify('going right')
            elif e.key.arrow_up:
                ui.notify('going up')
            elif e.key.arrow_down:
                ui.notify('going down')

    keyboard = ui.keyboard(on_key=handle_key)
    ui.label('Key events can be caught globally by using the keyboard element.')
    ui.checkbox('Track key events').bind_value_to(keyboard, 'active')


doc.reference(ui.keyboard)
