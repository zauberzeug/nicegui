from nicegui import background_tasks, ui


@ui.page('/')
async def _page():
    with ui.row():
        lang = ui.select([], label='Language').classes('w-64')
        theme = ui.select([], label='Theme').classes('w-64')

    cm = ui.codemirror('foo = [1, 2, 3]', theme='oneDark', min_height='200px', highlight_whitespace=True).classes('w-full')
    ui.input('Synced value').classes('w-full').bind_value(cm)
    cm.on_value_change(lambda: print(cm.value))

    lang.on_value_change(lambda: cm.set_language(lang.value))
    theme.on_value_change(lambda: cm.set_theme(theme.value))
    ui.switch('Enabled', value=True).bind_value_to(cm, 'enabled')

    async def setup_values():
        lang.options = await cm.supported_languages()
        lang.value = cm.language
        lang.update()

        theme.options = await cm.supported_themes()
        theme.update()
        theme.value = cm.theme

    background_tasks.create(setup_values())

ui.run(dark=True)
