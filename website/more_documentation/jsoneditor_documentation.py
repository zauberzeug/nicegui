from nicegui import ui


def main_demo() -> None:
    ui.jsoneditor(properties={'content': {
        'json': {
            'array': [1, 2, 3],
            'boolean': True,
            'color': '#82b92c',
            None: None,
            'number': 123,
            'object': {'a': 'b', 'c': 'd'},
            'time': 1575599819000,
            'string': 'Hello World'
        }}},
        on_select=lambda e: ui.notify(f'Select: {e}'),
        on_change=lambda e: ui.notify(f'Change: {e}'))
