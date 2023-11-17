from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    ui.number(label='Number', value=3.1415927, format='%.2f',
              on_change=lambda e: result.set_text(f'you entered: {e.value}'))
    result = ui.label()


def more() -> None:
    @text_demo('Clearable', '''
        The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.    
    ''')
    def clearable():
        i = ui.number(value=42).props('clearable')
        ui.label().bind_text_from(i, 'value')

    @text_demo('Number of digits', '''
        You can specify the number of digits using the `digits` parameter.
        A negative value means decimal places before the dot.
        The rounding takes place when the input loses focus,
        when sanitization parameters like min, max or digits change,
        or when `sanitize()` is called manually.
    ''')
    def integer():
        n = ui.number(value=3.14159265359, digits=5)
        n.sanitize()
