from nicegui import ui

from . import doc


@doc.demo(ui.refreshable)
def main_demo() -> None:
    import random

    numbers = []

    @ui.refreshable
    def number_ui() -> None:
        ui.label(', '.join(str(n) for n in sorted(numbers)))

    def add_number() -> None:
        numbers.append(random.randint(0, 100))
        number_ui.refresh()

    number_ui()
    ui.button('Add random number', on_click=add_number)


@doc.demo('Refreshable UI with parameters', '''
    Here is a demo of how to use the refreshable decorator to create a UI that can be refreshed with different parameters.
''')
def refreshable_with_parameters():
    from datetime import datetime

    import pytz

    @ui.refreshable
    def clock_ui(timezone: str):
        ui.label(f'Current time in {timezone}:')
        ui.label(datetime.now(tz=pytz.timezone(timezone)).strftime('%H:%M:%S'))

    clock_ui('Europe/Berlin')
    ui.button('Refresh', on_click=clock_ui.refresh)
    ui.button('Refresh for New York', on_click=lambda: clock_ui.refresh('America/New_York'))
    ui.button('Refresh for Tokyo', on_click=lambda: clock_ui.refresh('Asia/Tokyo'))


@doc.demo('Refreshable UI for input validation', '''
    Here is a demo of how to use the refreshable decorator to give feedback about the validity of user input.
''')
def input_validation():
    import re

    pwd = ui.input('Password', password=True, on_change=lambda: show_info.refresh())

    rules = {
        'Lowercase letter': lambda s: re.search(r'[a-z]', s),
        'Uppercase letter': lambda s: re.search(r'[A-Z]', s),
        'Digit': lambda s: re.search(r'\d', s),
        'Special character': lambda s: re.search(r"[!@#$%^&*(),.?':{}|<>]", s),
        'min. 8 characters': lambda s: len(s) >= 8,
    }

    @ui.refreshable
    def show_info():
        for rule, check in rules.items():
            with ui.row().classes('items-center gap-2'):
                if check(pwd.value or ''):
                    ui.icon('done', color='green')
                    ui.label(rule).classes('text-xs text-green strike-through')
                else:
                    ui.icon('radio_button_unchecked', color='red')
                    ui.label(rule).classes('text-xs text-red')

    show_info()


@doc.demo('Refreshable UI with reactive state', '''
    You can create reactive state variables with the `ui.state` function, like `count` and `color` in this demo.
    They can be used like normal variables for creating UI elements like the `ui.label`.
    Their corresponding setter functions can be used to set new values, which will automatically refresh the UI.
''')
def reactive_state():
    @ui.refreshable
    def counter(name: str):
        with ui.card():
            count, set_count = ui.state(0)
            color, set_color = ui.state('black')
            ui.label(f'{name} = {count}').classes(f'text-{color}')
            ui.button(f'{name} += 1', on_click=lambda: set_count(count + 1))
            ui.select(['black', 'red', 'green', 'blue'],
                      value=color, on_change=lambda e: set_color(e.value))

    with ui.row():
        counter('A')
        counter('B')


@doc.demo('Global scope', '''
    When defining a refreshable function in the global scope,
    every refreshable UI that is created by calling this function will share the same state.
    In this demo, `hello()` will show the name entered in the input field.
    When opening the page with a second browser or in incognito mode,
    both browsers will continue to show the same name, even if it is changed in one of them.
    See the "local scope" demos below for a way to create independent refreshable UIs instead.
''')
def global_scope():
    from nicegui import app

    @ui.refreshable
    def hello():
        ui.label(f'Hello {app.storage.user.get("name")}')

    @ui.page('/global_refreshable')
    def demo():
        ui.input('Name', on_change=hello.refresh).bind_value(app.storage.user, 'name')
        hello()

    ui.link('Open demo', demo)


@doc.demo('Local scope (1/3)', '''
    When defining a refreshable function in a local scope,
    refreshable UI that is created by calling this function will have independent state.
    In contrast to the "global scope" demo, the name entered in the input field will only be shown to the same user.
''')
def local_scope_1():
    from nicegui import app

    @ui.page('/local_refreshable_1')
    def demo():
        @ui.refreshable
        def hello():
            ui.label(f'Hello {app.storage.user.get("name")}')

        ui.input('Name', on_change=hello.refresh).bind_value(app.storage.user, 'name')
        hello()

    ui.link('Open demo', demo)


@doc.demo('Local scope (2/3)', '''
    In order to define refreshable UIs with local state outside of page functions,
    you can, e.g., define a class with a refreshable method.
    This way, you can create multiple instances of the class with independent state,
    because the `ui.refreshable` decorator acts on the class instance rather than the class itself.
''')
def local_scope_2():
    from nicegui import app

    class Greeting:
        @ui.refreshable
        def hello(self):
            ui.label(f'Hello {app.storage.user.get("name")}')

    @ui.page('/local_refreshable_2')
    def demo():
        greeting = Greeting()
        ui.input('Name', on_change=greeting.hello.refresh) \
            .bind_value(app.storage.user, 'name')
        greeting.hello()

    ui.link('Open demo', demo)


@doc.demo('Local scope (3/3)', '''
    As an alternative to the class definition shown above, you can also define the UI function in global scope,
    but apply the `ui.refreshable` decorator inside the page function.
    This way the refreshable UI will have independent state.
''')
def local_scope_3():
    from nicegui import app

    def hello():
        ui.label(f'Hello {app.storage.user.get("name")}')

    @ui.page('/local_refreshable_3')
    def demo():
        refreshable_hello = ui.refreshable(hello)
        ui.input('Name', on_change=refreshable_hello.refresh) \
            .bind_value(app.storage.user, 'name')
        refreshable_hello()

    ui.link('Open demo', demo)


doc.reference(ui.refreshable)
