from nicegui import ui

from . import doc


@doc.demo(ui.input)
def main_demo() -> None:
    ui.input(label='Text', placeholder='start typing',
             on_change=lambda e: result.set_text('you typed: ' + e.value),
             validation={'Input too long': lambda value: len(value) < 20})
    result = ui.label()


@doc.demo('Autocompletion', '''
    The `autocomplete` feature provides suggestions as you type, making input easier and faster.
    The parameter `options` is a list of strings that contains the available options that will appear.
''')
def autocomplete_demo():
    options = ['AutoComplete', 'NiceGUI', 'Awesome']
    ui.input(label='Text', placeholder='start typing', autocomplete=options)


@doc.demo('Clearable', '''
    The `clearable` prop from [Quasar](https://quasar.dev/) adds a button to the input that clears the text.
''')
def clearable():
    i = ui.input(value='some text').props('clearable')
    ui.label().bind_text_from(i, 'value')


@doc.demo('Styling', '''
    Quasar has a lot of [props to change the appearance](https://quasar.dev/vue-components/input).
    It is even possible to style the underlying input with `input-style` and `input-class` props
    and use the provided slots to add custom elements.
''')
def styling():
    ui.input(placeholder='start typing').props('rounded outlined dense')
    ui.input('styling', value='some text') \
        .props('input-style="color: blue" input-class="font-mono"')
    with ui.input(value='custom clear button').classes('w-64') as i:
        ui.button(color='orange-8', on_click=lambda: i.set_value(None), icon='delete') \
            .props('flat dense').bind_visibility_from(i, 'value')


@doc.demo('Input validation', '''
    You can validate the input in two ways:

    - by passing a callable that returns an error message or `None`, or
    - by passing a dictionary that maps error messages to callables that return `True` (error) or `False` (no error).
''')
def validation():
    ui.input('Name', validation=lambda value: 'Too short' if len(value) < 5 else None)
    ui.input('Name', validation={'Too short': lambda value: len(value) >= 5})


doc.reference(ui.input)
