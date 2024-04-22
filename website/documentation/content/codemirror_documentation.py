from nicegui import ui
from nicegui import background_tasks

from . import doc

code = '''
print("Edit me!")
'''.strip()


@doc.demo(ui.codemirror)
def main_demo() -> None:
    cm = ui.codemirror(code, theme='basicDark', min_height='100px').classes('w-full')

    language = ui.select([], label='Language', on_change=lambda: cm.set_language(language.value)).classes('w-64')
    theme = ui.select([], label='Theme', on_change=lambda: cm.set_theme(theme.value)).classes('w-64')

    async def setup_values():
        language.options = await cm.supported_languages()
        language.value = cm.language
        language.update()

        theme.options = await cm.supported_themes()
        theme.value = cm.theme
        theme.update()

    background_tasks.create(setup_values())


doc.reference(ui.codemirror)
