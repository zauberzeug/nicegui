from nicegui import ui

from . import doc


@doc.demo(ui.date)
def main_demo() -> None:
    ui.date(value='2023-01-01', on_change=lambda e: result.set_text(e.value))
    result = ui.label()


@doc.demo('Input element with date picker', '''
    This demo shows how to implement a date picker with an input element.
    We place an icon in the input element's append slot.
    When the icon is clicked, we open a menu with a date picker.

    The date is bound to the input element's value.
    So both the input element and the date picker will stay in sync whenever the date is changed.
''')
def date():
    with ui.input('Date') as date:
        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
        with ui.menu() as menu:
            ui.date().bind_value(date)


@doc.demo('Date filter', '''
    This demo shows how to filter the dates in a date picker.
    In order to pass a function to the date picker, we use the `:options` property.
    The leading `:` tells NiceGUI that the value is a JavaScript expression.
''')
def date_filter():
    ui.date().props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')


doc.reference(ui.date)
