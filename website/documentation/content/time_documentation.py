from nicegui import ui

from . import doc


@doc.demo(ui.time)
def main_demo() -> None:
    ui.time(value='12:00', on_change=lambda e: result.set_text(e.value))
    result = ui.label()


@doc.demo('Input element with time picker', '''
    This demo shows how to implement a time picker with an input element.
    We place an icon in the input element's append slot.
    When the icon is clicked, we open a menu with a time picker.
    [QMenu](https://quasar.dev/vue-components/menu)'s "no-parent-event" prop can be used
    to prevent a click within the text input itself to open the menu.
    As the menu doesn't come with a "Close" button by default, we can add one for convenience.

    The time is bound to the input element's value.
    So both the input element and the time picker will stay in sync whenever the time is changed.
''')
def time_picker_demo():
    with ui.input('Time') as time:
        with ui.menu().props('no-parent-event') as menu:
            with ui.time().props('format24h').bind_value(time):
                with ui.row().classes('justify-end'):
                    ui.button('Close', on_click=menu.close)
        with time.add_slot('append'):
            ui.icon('access_time').on('click', menu.open).classes('cursor-pointer')


doc.reference(ui.time)
