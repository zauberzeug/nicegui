from nicegui import ui

from . import doc


@doc.demo(ui.card)
def main_demo() -> None:
    with ui.card().tight():
        ui.image('https://picsum.photos/id/684/640/360')
        with ui.card_section():
            ui.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, ...')


@doc.demo('Card without shadow', '''
    You can remove the shadow from a card by adding the `no-shadow` class.
    The following demo shows a 1 pixel wide border instead.
''')
def card_without_shadow() -> None:
    with ui.card().classes('no-shadow border-[1px]'):
        ui.label('See, no shadow!')


doc.reference(ui.card)
