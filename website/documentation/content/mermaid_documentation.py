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
    list(ui.context.client.elements.values())[-1].props['config'] = {'securityLevel': 'loose'}  # HACK: for click_demo


@doc.demo('Handle node events', '''
    You can register to click events by adding a `click` directive to a node to call `nodeClick()`, this will trigger the callback defined at `on_node_click`.
    When a callback is specified the `config` is updated to include ``{"securityLevel": "loose"}`` to allow JavaScript execution.
''')
def click_demo() -> None:
    ui.mermaid('''
    graph LR;
        A((Click Me));
        B((Or Click Me));
        A --> B;
        click A call nodeClick()
        click B call nodeClick()
    ''', on_node_click=lambda e: ui.notify(e.args))


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
    list(ui.context.client.elements.values())[-1].props['config'] = {'securityLevel': 'loose'}  # HACK: for click_demo


doc.reference(ui.mermaid)
