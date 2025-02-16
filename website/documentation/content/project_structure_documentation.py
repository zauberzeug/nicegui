from nicegui import ui

from ..windows import bash_window, python_window
from . import doc

doc.text('Project Structure', '''
    The NiceGUI package provides a [pytest plugin](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
    which can be activated via `pytest_plugins = ['nicegui.testing.plugin']`.
    This makes specialized [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) available for testing your NiceGUI user interface.
    With the [`screen` fixture](/documentation/screen) you can run the tests through a headless browser (slow)
    and with the [`user` fixture](/documentation/user) fully simulated in Python (fast).
    If you only want one kind of test fixtures,
    you can also use the plugin `nicegui.testing.user_plugin` or `nicegui.testing.screen_plugin`.

    There are a multitude of ways to structure your project and tests.
    Here we only present two approaches which we found useful,
    one for [small apps and experiments](/documentation/project_structure#simple)
    and a [modular one for larger projects](/documentation/project_structure#modular).
    You can find more information in the [pytest documentation](https://docs.pytest.org/en/stable/contents.html).
''')

doc.text('Simple', '''
    For small apps and experiments you can put the tests in a separate file,
    as we do in the examples
    [Chat App](https://github.com/zauberzeug/nicegui/tree/main/examples/chat_app)
    [Todo List](https://github.com/zauberzeug/nicegui/tree/main/examples/todo_list/) and
    [Authentication](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication).
    To properly re-initialize your `main.py` in the tests,
    you place an empty `__init__.py` file next to your code to make it a package
    and use the `module_under_test` marker to automatically reload your main file for each test.
    Also don't forget the `pytest.ini` file
    to enable the [`asyncio_mode = auto`](/documentation/user#async_execution) option for the user fixture
    and make sure you properly guard the `ui.run()` call in your `main.py`
    to prevent the server from starting during the tests:
''')


@doc.ui
def simple_project_code():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]'):
            ui.markdown('''
                ```python
                from nicegui import ui

                def hello() -> None:
                    ui.notify('Hello World!')

                ui.button('Click me', on_click=hello)

                if __name__ in {'__main__', '__mp_main__'}:
                    ui.run()
                ```
            ''')

        with python_window(classes='w-[400px]', title='test_app.py'):
            ui.markdown('''
                ```python
                import pytest
                from nicegui import ui
                from nicegui.testing import User
                from . import main

                pytest_plugins = ['nicegui.testing.user_plugin']

                @pytest.mark.module_under_test(main)
                async def test_click(user: User) -> None:
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
            ''')


@doc.ui
def simple_project_bash():
    with bash_window(classes='max-w-[820px] w-full h-42'):
        ui.markdown('''
            ```bash
            $ ls
            __init__.py         main.py        test_app.py       pytest.ini

            $ pytest
            ==================== test session starts =====================
            test_app.py .                                     [100%]
            ===================== 1 passed in 0.51 s ======================
            ```
        ''')


doc.text('Modular', '''
    A more modular approach is to create a package for your code with an empty `__init__.py`
    and a separate `tests` folder for your tests.
    In your package a `startup.py` file can be used to register pages and do all necessary app initialization.
    The `main.py` at root level then only imports the startup routine and calls `ui.run()`.
    An empty `conftest.py` file in the root directory makes the package with its `startup` routine available to the tests.
    Also don't forget the `pytest.ini` file
    to enable the [`asyncio_mode = auto`](/documentation/user#async_execution) option for the user fixture.
''')


@doc.ui
def modular_project():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]'):
            ui.markdown('''
                ```python
                from nicegui import ui, app
                from app.startup import startup

                app.on_startup(startup)

                ui.run()
                ```
            ''')

        with python_window(classes='w-[400px]', title='app/startup.py'):
            ui.markdown('''
                ```python
                from nicegui import ui

                def hello() -> None:
                    ui.notify('Hello World!')

                def startup() -> None:
                    @ui.page('/')
                    def index():
                        ui.button('Click me', on_click=hello)
                ```
            ''')

    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='tests/test_app.py'):
            ui.markdown('''
                ```python
                from nicegui import ui
                from nicegui.testing import User
                from app.startup import startup

                pytest_plugins = ['nicegui.testing.user_plugin']

                async def test_click(user: User) -> None:
                    startup()
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
                ''')

        with bash_window(classes='w-[400px]'):
            ui.markdown('''
                ```bash
                $ tree
                .
                ├── main.py
                ├── pytest.ini
                ├── app
                │   ├── __init__.py
                │   └── startup.py
                └── tests
                    ├── conftest.py
                    └── test_app.py
                ```
            ''')


doc.text('', '''
    You can also define your own fixtures in the `conftest.py` which call the `startup` routine.
    Pytest has some magic to automatically find and use this specialized fixture in your tests.
    This way you can keep your tests clean and simple.
    See the [pytests example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)
    for a full demonstration of this setup.
''')


@doc.ui
def custom_user_fixture():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='tests/test_app.py'):
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

        with python_window(classes='w-[400px]', title='conftest.py'):
            ui.markdown('''
                ```python
                import pytest
                from nicegui.testing import User
                from app.startup import startup

                pytest_plugins = ['nicegui.testing.user_plugin']

                @pytest.fixture
                def user(user: User) -> User:
                    startup()
                    return user
                ```
            ''')
