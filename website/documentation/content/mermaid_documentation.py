from nicegui import ui

from . import doc


@doc.demo(ui.mermaid)
def main_demo() -> None:
    ui.mermaid('''
    graph LR;
        A --> B;
        A --> C;
    ''')
    # END OF DEMO
    list(ui.context.client.elements.values())[-1]._props['config'] = {'securityLevel': 'loose'}  # HACK: for click_demo


@doc.demo('Handle click events', '''
    You can register to click events by adding a `click` directive to a node and emitting a custom event.
    Make sure to set the `securityLevel` to `loose` in the `config` parameter to allow JavaScript execution.
''')
def click_demo() -> None:
    ui.mermaid('''
    graph LR;
        A((Click me!));
        click A call emitEvent("mermaid_click", "You clicked me!")
    ''', config={'securityLevel': 'loose'})
    ui.on('mermaid_click', lambda e: ui.notify(e.args))


@doc.demo('Handle errors', '''
    You can handle errors by listening to the `error` event.
    The event `args` contain the properties `hash`, `message`, `str` and an `error` object with additional information.
''')
def error_demo() -> None:
    ui.mermaid('''
    graph LR;
        A --> B;
        A -> C;
    ''').on('error', lambda e: print(e.args['message']))
    # END OF DEMO
    list(ui.context.client.elements.values())[-1]._props['config'] = {'securityLevel': 'loose'}  # HACK: for click_demo


doc.reference(ui.mermaid)
