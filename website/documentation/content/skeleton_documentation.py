from nicegui import ui

from . import doc


@doc.demo(ui.skeleton)
def skeleton():
    ui.skeleton().classes('w-full')


@doc.demo('Styling and animation', '''
    The `square` and `bordered` parameters can be set to `True` to remove the border-radius and add a border to the skeleton.

    The `animation` parameter can be set to "pulse", "wave", "pulse-x", "pulse-y", "fade", "blink", or "none"
    to change the animation effect.
    The default value is "wave".
''')
def custom_animations():
    ui.skeleton('QToolbar', square=True, bordered=True, animation='pulse-y') \
        .classes('w-full')


@doc.demo('YouTube Skeleton', '''
    Here is an example skeleton for a YouTube video.
''')
def youtube_skeleton():
    with ui.card().tight().classes('w-full'):
        ui.skeleton(square=True, animation='fade', height='150px', width='100%')
        with ui.card_section().classes('w-full'):
            ui.skeleton('text').classes('text-subtitle1')
            ui.skeleton('text').classes('text-subtitle1 w-1/2')
            ui.skeleton('text').classes('text-caption')
