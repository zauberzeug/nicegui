from nicegui import ui

from . import doc


@doc.demo(ui.codemirror)
def main_demo() -> None:
    editor = ui.codemirror('print("Edit me!")', language='Python').classes('h-32')
    ui.select(editor.supported_languages, label='Language', clearable=True) \
        .classes('w-32').bind_value(editor, 'language')
    ui.select(editor.supported_themes, label='Theme') \
        .classes('w-32').bind_value(editor, 'theme')
    ui.checkbox('Wrap Lines', value=editor.line_wrapping,
                on_change=lambda e: editor.set_line_wrapping(e.value))


@doc.demo(
    'Custom Completions',
    '''
    You can provide custom autocompletion suggestions using the ``custom_completions`` parameter.
    Each completion is a dictionary with keys: ``label`` (required), ``detail``, ``info``, ``apply``, and ``type``.
    Completions appear when typing text that matches the label.
''',
)
def custom_completions_demo() -> None:
    completions = [
        {
            'label': 'greet',
            'detail': '(name: str)',
            'info': 'Greet someone by name',
            'apply': 'greet("World")',
            'type': 'function',
        },
        {
            'label': 'farewell',
            'detail': '(name: str)',
            'info': 'Say goodbye to someone',
            'apply': 'farewell("World")',
            'type': 'function',
        },
        {
            'label': 'message',
            'detail': 'str',
            'info': 'A message variable',
            'apply': 'message',
            'type': 'variable',
        },
    ]
    ui.codemirror(
        '# Type "gr" or "fa" to see completions\n', language='Python', custom_completions=completions,
    ).classes('h-32')


@doc.demo(
    'Dynamic Completions',
    '''
    Completions can be updated dynamically using the ``set_completions()`` method.
    This allows adding context-aware completions based on application state.
''',
)
def dynamic_completions_demo() -> None:
    editor = ui.codemirror('# Click buttons to change completions\n', language='Python').classes('h-32')

    math_completions = [
        {'label': 'math.sin', 'detail': '(x)', 'type': 'function'},
        {'label': 'math.cos', 'detail': '(x)', 'type': 'function'},
        {'label': 'math.pi', 'detail': 'float', 'type': 'variable'},
    ]

    string_completions = [
        {'label': 'str.upper', 'detail': '()', 'type': 'function'},
        {'label': 'str.lower', 'detail': '()', 'type': 'function'},
        {'label': 'str.split', 'detail': '(sep)', 'type': 'function'},
    ]

    with ui.row():
        ui.button('Math', on_click=lambda: editor.set_completions(math_completions))
        ui.button('String', on_click=lambda: editor.set_completions(string_completions))
        ui.button('Clear', on_click=lambda: editor.set_completions([]))


@doc.demo('Preserving Cursor Position', '''
    ``set_value`` applies only the modified region, so cursor positions and selections outside the change are preserved.
    Try editing the code below while the first line updates automatically.
''')
def preserve_cursor_demo() -> None:
    from datetime import datetime

    editor = ui.codemirror(f'# {datetime.now():%H:%M:%S}\n', language='Python')
    ui.timer(1, lambda: editor.set_value(
        f'# {datetime.now():%H:%M:%S}\n' + editor.value.split('\n', 1)[-1]
    ))


doc.reference(ui.codemirror)
