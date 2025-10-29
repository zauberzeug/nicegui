from nicegui import ui

from . import doc


@doc.demo(ui.element)
def main_demo() -> None:
    with ui.element('div').classes('p-2 bg-blue-100'):
        ui.label('inside a colored div')


@doc.demo('Register event handlers', '''
    The event handler can be a Python function, a JavaScript function or a combination of both:

    - If you want to handle the event on the server with all (serializable) event arguments,
        use a Python ``handler``.

    - If you want to handle the event on the client side without emitting anything to the server,
        use ``js_handler`` with a JavaScript function handling the event.

    - If you want to handle the event on the server with a subset or transformed version of the event arguments,
        use ``js_handler`` with a JavaScript function emitting the transformed arguments using ``emit()``, and
        use a Python ``handler`` to handle these arguments on the server side.

        The ``js_handler`` can also decide to selectively emit arguments to the server,
        in which case the Python ``handler`` will not always be called.

    *Updated in version 2.18.0: Both handlers can be specified at the same time.*
''')
def register_event_handlers() -> None:
    ui.button('Python handler') \
        .on('click',
            lambda e: ui.notify(f'click: ({e.args["clientX"]}, {e.args["clientY"]})'))

    ui.button('JavaScript handler') \
        .on('click',
            js_handler='(e) => alert(`click: (${e.clientX}, ${e.clientY})`)')

    ui.button('Combination') \
        .on('click',
            lambda e: ui.notify(f'click: {e.args}'),
            js_handler='(e) => emit(e.clientX, e.clientY)')


@doc.demo('Move elements', '''
    This demo shows how to move elements between or within containers.
''')
def move_elements() -> None:
    with ui.card() as a:
        ui.label('A')
        x = ui.label('X')

    with ui.card() as b:
        ui.label('B')

    ui.button('Move X to A', on_click=lambda: x.move(a))
    ui.button('Move X to B', on_click=lambda: x.move(b))
    ui.button('Move X to top', on_click=lambda: x.move(target_index=0))


@doc.demo('Move elements to slots', '''
    This demo shows how to move elements between slots within an element.
''')
def move_elements_to_slots() -> None:
    with ui.card() as card:
        name = ui.input('Name', value='Paul')
        name.add_slot('append')
        icon = ui.icon('face')

    ui.button('Move into input', on_click=lambda: icon.move(name, target_slot='append'))
    ui.button('Move out of input', on_click=lambda: icon.move(card))


@doc.demo('Default props', '''
    You can set default props for all elements of a certain class.
    This way you can avoid repeating the same props over and over again.

    Default props only apply to elements created after the default props were set.
    Subclasses inherit the default props of their parent class.
''')
def default_props() -> None:
    ui.button.default_props('rounded outline')
    ui.button('Button A')
    ui.button('Button B')
    # END OF DEMO
    ui.button.default_props(remove='rounded outline')


@doc.demo('Default classes', '''
    You can set default classes for all elements of a certain class.
    This way you can avoid repeating the same classes over and over again.

    Default classes only apply to elements created after the default classes were set.
    Subclasses inherit the default classes of their parent class.
''')
def default_classes() -> None:
    ui.label.default_classes('bg-blue-100 p-2')
    ui.label('Label A')
    ui.label('Label B')
    # END OF DEMO
    ui.label.default_classes(remove='bg-blue-100 p-2')


@doc.demo('Default style', '''
    You can set a default style for all elements of a certain class.
    This way you can avoid repeating the same style over and over again.

    A default style only applies to elements created after the default style was set.
    Subclasses inherit the default style of their parent class.
''')
def default_style() -> None:
    ui.label.default_style('color: tomato')
    ui.label('Label A')
    ui.label('Label B')
    # END OF DEMO
    ui.label.default_style(remove='color: tomato')


doc.reference(ui.element)
