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
    - by passing a dictionary that maps error messages to callables that return `True` if the input is valid.

    Both of these validations **run on Python-side**, bringing security against client-side circumventions and flexibility in validation logic.
    However they do not correspond to Quasar's validation-related props and methods, and require server communication and processing.

    *Since version 2.7.0:*
    The callable validation function can also be an async coroutine.
    In this case, the validation is performed asynchronously in the background.

    You can use the `validate` method of the input element to trigger the validation manually.
    It returns `True` if the input is valid, and an error message otherwise.
    For async validation functions, the return value must be explicitly disabled by setting `return_result=False`.
''')
def validation():
    ui.input('Name', validation=lambda value: 'Too short' if len(value) < 5 else None)
    ui.input('Name', validation={'Too short': lambda value: len(value) >= 5})


@doc.demo('Lazy validation', '''
    To run validation lazily, you can consider:

    - adding a debounce with the `debounce` prop, so that validation is only triggered after the user stops typing for a certain amount of time,
    - disable automatic validation with `without_auto_validation()` and call the `validate` method manually whenever appropriate, e.g., on blur, on form submission,
    - or a combination of both approaches.
''')
def lazy_validation():
    ui.input('name (debounce)', validation={'Too short': lambda v: len(v) > 5}).props('debounce=1000')

    name = ui.input('name (on blur)', validation={'Too short': lambda v: len(v) > 5}).without_auto_validation()
    name.on('blur', name.validate)


@doc.demo('Client-side validation', '''
    Trading performance for security and flexibility, you can also use Quasar's client-side validation
    by passing the `rules` prop with Quasar-compatible rules.

    This way the Quasar props such as `lazy-rules` and methods such as `resetValidation` can also be used.

    Note the use of `:` prefix to denote a JavaScript expression string, and treating `props` as a dictionary to simplify string-escaping.
''')
def client_side_validation():
    name = ui.input('name (client-side)').props('lazy-rules')
    name.props[':rules'] = '''[ val => val.length > 5 || 'Too short' ]'''
    ui.button('Reset Validation', on_click=lambda: name.run_method('resetValidation'))


doc.reference(ui.input)
