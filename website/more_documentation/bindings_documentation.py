from nicegui import ui
from ..documentation_tools import text_demo

def main_demo() -> None:
    class Demo:
        def __init__(self):
            self.number = 1

    demo = Demo()
    v = ui.checkbox('visible', value=True)
    with ui.column().bind_visibility_from(v, 'value'):
        ui.slider(min=1, max=3).bind_value(demo, 'number')
        ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
        ui.number().bind_value(demo, 'number')

def more() -> None:
    @text_demo('Bind to dictionary')
    def bind_dictionary():
        dictionary = {'name': 'NiceGUI', 'age': 2}

        with ui.grid(columns=2):
            ui.label('Name:')
            ui.label().bind_text_from(dictionary, 'name')

            ui.label('Age:')
            ui.label().bind_text_from(dictionary, 'age')

        def nicegui_older():
            dictionary['age'] += 1

        ui.button('Make NiceGUI older!', on_click=nicegui_older)

    @text_demo('Bind to variable', '''Here we are binding the value from the datepicker to a bare variable. [Using official datepicker example](https://nicegui.io/documentation/date#input_element_with_date_picker)''')
    def bind_variable():
        today_date = '1970-01-01'

        def notify_date():
            global today_date
            ui.notify(f'Today is: {today_date}')
            
        with ui.input('Date') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date(on_change=notify_date).bind_value(date).bind_value(globals(), 'today_date')
