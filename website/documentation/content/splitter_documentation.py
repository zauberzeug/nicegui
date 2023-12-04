from nicegui import ui

from . import doc


@doc.demo(ui.splitter)
def main_demo() -> None:
    with ui.splitter() as splitter:
        with splitter.before:
            ui.label('This is some content on the left hand side.').classes('mr-2')
        with splitter.after:
            ui.label('This is some content on the right hand side.').classes('ml-2')


@doc.demo('Advanced usage', '''
    This demo shows all the slots and parameters including a tooltip, a custom separator, and a callback.
''')
def advanced_usage() -> None:
    with ui.splitter(horizontal=False, reverse=False, value=60,
                     on_change=lambda e: ui.notify(e.value)) as splitter:
        ui.tooltip('This is the default slot.').classes('bg-green')
        with splitter.before:
            ui.label('This is the left hand side.').classes('mr-2')
        with splitter.after:
            ui.label('This is the right hand side.').classes('ml-2')
        with splitter.separator:
            ui.icon('lightbulb').classes('text-green')

    ui.number('Split value', format='%.1f').bind_value(splitter)


@doc.demo('Image fun', '''
    This demo shows how to use the splitter to display images side by side.
''')
def image_fun() -> None:
    with ui.splitter().classes('w-72 h-48') \
            .props('before-class=overflow-hidden after-class=overflow-hidden') as splitter:
        with splitter.before:
            ui.image('https://cdn.quasar.dev/img/parallax1.jpg').classes('w-72 absolute-top-left')
        with splitter.after:
            ui.image('https://cdn.quasar.dev/img/parallax1-bw.jpg').classes('w-72 absolute-top-right')


doc.reference(ui.splitter)
