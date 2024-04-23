from nicegui import ui
from nicegui import background_tasks

from . import doc


@doc.demo(ui.codemirror)
def main_demo() -> None:
    editor = ui.codemirror('print("Edit me!")', theme='basicDark',
                           language='Python', min_height='100px').classes('w-full')

    language = ui.select([], label='Language', on_change=lambda: editor.set_language(language.value)).classes('w-64')
    theme = ui.select([], label='Theme', on_change=lambda: editor.set_theme(theme.value)).classes('w-64')

    async def setup_values():
        language.options = await editor.supported_languages()
        language.value = editor.language
        language.update()

        theme.options = await editor.supported_themes()
        theme.value = editor.theme
        theme.update()

    background_tasks.create(setup_values())


doc.reference(ui.codemirror)
