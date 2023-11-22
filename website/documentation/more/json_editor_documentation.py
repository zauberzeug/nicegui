from nicegui import ui


def main_demo() -> None:
    json = {
        'array': [1, 2, 3],
        'boolean': True,
        'color': '#82b92c',
        None: None,
        'number': 123,
        'object': {
            'a': 'b',
            'c': 'd',
        },
        'time': 1575599819000,
        'string': 'Hello World',
    }
    ui.json_editor({'content': {'json': json}},
                   on_select=lambda e: ui.notify(f'Select: {e}'),
                   on_change=lambda e: ui.notify(f'Change: {e}'))
