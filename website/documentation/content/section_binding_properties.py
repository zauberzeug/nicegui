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


@doc.demo('Bindable properties for maximum performance', '''
    There are two types of bindings:

    1. "Bindable properties" automatically detect write access and trigger the value propagation.
        Most NiceGUI elements use these bindable properties, like `value` in `ui.input` or `text` in `ui.label`.
        Basically all properties with `bind()` methods support this type of binding.
    2. All other bindings are sometimes called "active links".
        If you bind a label text to some dictionary entry or an attribute of a custom data model,
        NiceGUI's binding module has to actively check if the value changed.
        This is done in a `refresh_loop()` which runs every 0.1 seconds.
        The interval can be configured via `binding_refresh_interval` in `ui.run()`.

    The "bindable properties" are very efficient and don't cost anything as long as the values don't change.
    But the "active links" need to check all bound values 10 times per second.
    This can get costly, especially if you bind to complex objects like lists or dictionaries.

    Because it is crucial not to block the main thread for too long,
    we show a warning if one step of the `refresh_loop()` takes too long.
    You can configure the threshold via `binding.MAX_PROPAGATION_TIME` which defaults to 0.01 seconds.
    But often the warning is a valuable indicator for a performance or memory issue.
    If your CPU would be busy updating bindings a significant duration,
    nothing else could happen on the main thread and the UI "hangs".

    The following demo shows how to define and use bindable properties for a `Demo` class like in the first demo.
    The `number` property is now a `BindableProperty`,
    which allows NiceGUI to detect write access and trigger the value propagation immediately.
''')
def bindable_properties():
    from nicegui import binding

    class Demo:
        number = binding.BindableProperty()

        def __init__(self):
            self.number = 1

    demo = Demo()
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
    ui.number(min=1, max=3).bind_value(demo, 'number')


@doc.demo('Bindable dataclass', '''
    The `bindable_dataclass` decorator provides a convenient way to create classes with bindable properties.
    It extends the functionality of Python's standard `dataclasses.dataclass` decorator
    by automatically making all dataclass fields bindable.
    This eliminates the need to manually declare each field as a `BindableProperty`
    while retaining all the benefits of regular dataclasses.

    *Added in version 2.11.0*
''')
def bindable_dataclass():
    from nicegui import binding

    @binding.bindable_dataclass
    class Demo:
        number: int = 1

    demo = Demo()
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'A', 2: 'B', 3: 'C'}).bind_value(demo, 'number')
    ui.number(min=1, max=3).bind_value(demo, 'number')
