from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.input(label='Text', placeholder='start typing',
             on_change=lambda e: result.set_text('you typed: ' + e.value),
             validation={'Input too long': lambda value: len(value) < 20})
    result = ui.label()


def more() -> None:

    @text_demo('Autocompletion', '''
        The `autocomplete` feature provides suggestions as you type, making input easier and faster.
        The parameter `options` is a list of strings that contains the available options that will appear.
    ''')
    async def autocomplete_demo():
        options = ['AutoComplete', 'NiceGUI', 'Awesome']
        ui.input(label='Text', placeholder='start typing', autocomplete=options)

    @text_demo('Clearable', '''
        The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.    
    ''')
    async def clearable():
        i = ui.input(value='some text').props('clearable')
        ui.label().bind_text_from(i, 'value')
