from collections.abc import Callable

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


@doc.demo('Collaborative Editor', '''
    Multiple users can edit the same document simultaneously.
    A shared ``Event`` notifies all editors when the content changes.

    *Since version 3.8.0:*
    ``set_value`` applies only the modified region to preserve cursor positions.
''')
def collaborative_editor_demo() -> Callable:
    from nicegui import Event, events

    document = {'value': 'print("Hello, world!")'}
    change = Event[str]()

    def root():
        def on_change(e: events.ValueChangeEventArguments) -> None:
            document['value'] = e.value
            change.emit(e.value)

        editor = ui.codemirror(value=document['value'], on_change=on_change)
        change.subscribe(editor.set_value)

    return root


doc.reference(ui.codemirror)
