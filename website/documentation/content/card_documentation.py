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

    Alternatively, you can use Quasar's "flat" and "bordered" props to achieve the same effect.
''')
def card_without_shadow() -> None:
    with ui.card().classes('no-shadow border border-gray-200'):
        ui.label('See, no shadow!')

    with ui.card().props('flat bordered'):
        ui.label('Also no shadow!')


@doc.demo('Tight card layout', '''
    By default, cards have a padding.
    You can remove the padding and gaps between nested elements by using the `tight` method.
    This also hides outer borders and shadows of nested elements, like in an original QCard.
''')
def custom_context_menu() -> None:
    rows = [{'age': '16'}, {'age': '18'}, {'age': '21'}]

    with ui.row():
        with ui.card():
            ui.table(rows=rows).props('flat bordered')

        with ui.card().tight():
            ui.table(rows=rows).props('flat bordered')


doc.reference(ui.card)
