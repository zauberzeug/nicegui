from nicegui import ui

from . import doc

date = '2023-01-01'

doc.title('*Binding* Properties')


@doc.demo('Bindings', '''
    NiceGUI is able to directly bind UI elements to models.
    Binding is possible for UI element properties like text, value or visibility and for model properties that are (nested) class attributes.
    Each element provides methods like `bind_value` and `bind_visibility` to create a two-way binding with the corresponding property.
    To define a one-way binding use the `_from` and `_to` variants of these methods.
    Just pass a property of the model as parameter to these methods to create the binding.
    The values will be updated immediately and whenever one of them changes.
''')
def bindings_demo():
    class Demo:
        def __init__(self):
            self.number = 1

    demo = Demo()
    v = ui.checkbox('visible', value=True)
    with ui.column().bind_visibility_from(v, 'value'):
        ui.slider(min=1, max=3).bind_value(demo, 'number')
        ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
        ui.number().bind_value(demo, 'number')


@doc.demo('Bind to dictionary', '''
    Here we are binding the text of labels to a dictionary.
''')
def bind_dictionary():
    data = {'name': 'Bob', 'age': 17}

    ui.label().bind_text_from(data, 'name', backward=lambda n: f'Name: {n}')
    ui.label().bind_text_from(data, 'age', backward=lambda a: f'Age: {a}')

    ui.button('Turn 18', on_click=lambda: data.update(age=18))


@doc.demo('Bind to variable', '''
    Here we are binding the value from the datepicker to a bare variable.
    Therefore we use the dictionary `globals()` which contains all global variables.
    This demo is based on the [official datepicker example](/documentation/date#input_element_with_date_picker).
''')
def bind_variable():
    # date = '2023-01-01'

    with ui.input('Date').bind_value(globals(), 'date') as date_input:
        with ui.menu() as menu:
            ui.date(on_change=lambda: ui.notify(f'Date: {date}')).bind_value(date_input)
        with date_input.add_slot('append'):
            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')


@doc.demo('Bind to storage', '''
    Bindings also work with [`app.storage`](/documentation/storage).
    Here we are storing the value of a textarea between visits.
    The note is also shared between all tabs of the same user.
''')
def ui_state():
    from nicegui import app

    # @ui.page('/')
    # def index():
    #     ui.textarea('This note is kept between visits')
    #         .classes('w-full').bind_value(app.storage.user, 'note')
    # END OF DEMO
    ui.textarea('This note is kept between visits').classes('w-full').bind_value(app.storage.user, 'note')
