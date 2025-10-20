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


@doc.demo('Prevent default and stop propagation', '''
    You can use the `js_handler` parameter of the `on` method to control how an event is handled on the client side.
    To prevent the default behavior, you can call the `preventDefault` method of the `event` object.
    To stop the propagation of the event, you could also call the `stopPropagation` method of the `event` object.

    *Added in version 3.1.0*
''')
def prevent_default() -> None:
    ui.label('Select via Ctrl-A or Cmd-A is disabled')

    ui.keyboard() \
        .on('key', lambda: ui.notify('Select all prevented.'), js_handler='''(e) => {
            if (e.key === 'a' && (e.ctrlKey || e.metaKey) && e.action === 'keydown') {
                emit(e);
                e.event.preventDefault();
            }
        }''')


doc.reference(ui.keyboard)
