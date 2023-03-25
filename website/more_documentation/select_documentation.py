from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    select1 = ui.select([1, 2, 3], value=1)
    select2 = ui.select({1: 'One', 2: 'Two', 3: 'Three'}).bind_value(select1, 'value')


def more() -> None:
    @text_demo('Search-as-you-type', '''
        You can activate `with_input` to get a text input with autocompletion.
        The options will be filtered as you type.
    ''')
    def search_as_you_type():
        continents = [
            'Asia',
            'Africa',
            'Antarctica',
            'Europe',
            'Oceania',
            'North America',
            'South America',
        ]
        ui.select(options=continents, with_input=True,
                  on_change=lambda e: ui.notify(e.value)).classes('w-40')
