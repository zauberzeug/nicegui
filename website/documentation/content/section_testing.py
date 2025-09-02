from . import (
    doc,
    screen_documentation,
    user_documentation,
)

from ..windows import python_window
from nicegui import ui

doc.title('*Testing*')

doc.redirects['project_structure_documentation'] = 'section_testing'
doc.text('Running Integration Tests', '''
    The NiceGUI package provides a [pytest plugin](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
    which can be activated via `-p nicegui.testing.plugin` parameter.
    This makes specialized [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
    available which allows you to write integration tests for your NiceGUI user interface.
    With the [`screen` fixture](/documentation/screen) you can run integration tests through a headless browser (slow).
    On the other hand the [`user` fixture](/documentation/user) allows integration tests to be fully simulated in Python (fast).
    If you only want one kind of test fixtures,
    you can also use the plugin `nicegui.testing.user_plugin` or `nicegui.testing.screen_plugin`.

    There are a multitude of ways to structure your project and tests.
    Here we only present our preferred approach for small and large projects which is on the one hand very easy but yet super powerful.
    For other approaches please check the [pytest documentation](https://docs.pytest.org/en/stable/contents.html).
''')

doc.text('Set main file in pytest.ini', '''
    The trick is to place a `pytest.ini` in the root of your project and configure it to load the NiceGUI testing plugin,
    set [`asyncio_mode = auto`](/documentation/user#async_execution)
    and configure `main_file` in the `pytest.ini` (default is `main.py`).
    The `main_file` will automatically be used as an entry point for each integration test (user or screen fixture).

    *Added in version 3.0.0.*
    ''')


@doc.ui
def project_code():
    with python_window(classes='max-w-[820px] w-full h-48'):
        ui.markdown('''
            ```python
            from nicegui import ui

            def root() -> None:
                ui.button('Click me', lambda: ui.notify('Hello World!'))

            if __name__ in {'__main__', '__mp_main__'}:
                ui.run(root)
            ```
        ''')


@doc.ui
def project_pytest():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='test_app.py'):
            ui.markdown('''
                ```python
                from nicegui import ui
                from nicegui.testing import User

                async def test_click(user: User) -> None:
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
            ''')
        with python_window(classes='w-[400px]', title='pytest.ini'):
            ui.markdown('''
                ```ini
                [pytest]
                asyncio_mode = auto
                main_file = main.py
                addopts = -p nicegui.testing.plugin
                ```
            ''')


doc.text('', '''
    Please also have a look at the examples
    [Chat App](https://github.com/zauberzeug/nicegui/tree/main/examples/chat_app),
    [Todo List](https://github.com/zauberzeug/nicegui/tree/main/examples/todo_list/),
    [Authentication](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication)
    and our [more complex pytest example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)
    for demonstration.
''')


doc.intro(user_documentation)
doc.intro(screen_documentation)
