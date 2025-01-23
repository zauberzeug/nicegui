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
    [QMenu](https://quasar.dev/vue-components/menu)'s "no-parent-event" prop is used
    to prevent opening the menu when clicking into the input field.
    As the menu doesn't come with a "Close" button by default, we add one for convenience.

    The date is bound to the input element's value.
    So both the input element and the date picker will stay in sync whenever the date is changed.
''')
def date_picker_demo():
    with ui.input('Date') as date:
        with ui.menu().props('no-parent-event') as menu:
            with ui.date().bind_value(date):
                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close).props('flat')
        with date.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')


@doc.demo('Date range input', '''
    You can use the "range" prop to select a range of dates.
    The `value` will be a dictionary with "from" and "to" keys.
    The following demo shows how to bind a date range picker to an input element,
    using the `forward` and `backward` functions to convert between the date picker's dictionary and the input string.
''')
def date_range_input():
    date_input = ui.input('Date range').classes('w-40')
    ui.date().props('range').bind_value(
        date_input,
        forward=lambda x: f'{x["from"]} - {x["to"]}' if x else None,
        backward=lambda x: {
            'from': x.split(' - ')[0],
            'to': x.split(' - ')[1],
        } if ' - ' in (x or '') else None,
    )


@doc.demo('Date filter', '''
    This demo shows how to filter the dates in a date picker.
    In order to pass a function to the date picker, we use the `:options` property.
    The leading `:` tells NiceGUI that the value is a JavaScript expression.
''')
def date_filter():
    ui.date().props('''default-year-month=2023/01 :options="date => date <= '2023/01/15'"''')


doc.reference(ui.date)
