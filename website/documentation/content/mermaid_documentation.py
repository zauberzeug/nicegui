from nicegui import ui

from . import doc


@doc.demo(ui.mermaid)
def main_demo() -> None:
    ui.mermaid('''
    graph LR;
        A --> B;
        A --> C;
    ''')


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


doc.reference(ui.mermaid)
