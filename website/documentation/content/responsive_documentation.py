from nicegui import ui

from . import doc

doc.text('Usage notes', '''
    - Quasar's Responsive component only supports a single direct child. Wrap multiple elements in an additional container such as ``ui.column`` or ``ui.row``.
    - Avoid wrapping components that already expose a ``ratio`` parameter (e.g. ``ui.image`` or ``ui.video``) or components with a forced height.
    - When passing the ratio as a string, provide the decimal result directly (e.g. ``"1.7777"`` instead of ``"16/9"``).
''')


@doc.demo(ui.responsive)
def main_demo() -> None:
    with ui.responsive(ratio=16 / 9):
        with ui.card():
            ui.icon('live_tv')
            ui.label('16:9 content')


doc.reference(ui.responsive)
