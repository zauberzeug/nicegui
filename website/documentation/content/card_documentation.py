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


@doc.demo('The issue with nested borders', '''
    The following example shows a table nested in a card.
    Cards have a default padding in NiceGUI, so the table is not flush with the card's border.
    The table has the `flat` and `bordered` props set, so it should have a border.
    However, due to the way QCard is designed, the border is not visible (first card).
    There are two ways to fix this:

    - To get the original QCard behavior, use the `tight` method (second card).
        It removes the padding and the table border collapses with the card border.

    - To preserve the padding _and_ the table border, move the table into another container like a `ui.row` (third card).

    See https://github.com/zauberzeug/nicegui/issues/726 for more information.
''')
def custom_context_menu() -> None:
    columns = [{'name': 'age', 'label': 'Age', 'field': 'age'}]
    rows = [{'age': '16'}, {'age': '18'}, {'age': '21'}]

    with ui.row():
        with ui.card():
            ui.table(columns, rows).props('flat bordered')

        with ui.card().tight():
            ui.table(columns, rows).props('flat bordered')

        with ui.card():
            with ui.row():
                ui.table(columns, rows).props('flat bordered')


doc.reference(ui.card)
