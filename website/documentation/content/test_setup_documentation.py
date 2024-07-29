from nicegui import ui

from ..windows import bash_window, python_window
from . import doc

doc.title('Project Structure')


doc.text('Setup', '''
    The NiceGUI package comes with [pytest plugin](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
    which automatically provides [fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) for testing your user interface.
    You can run the tests through a browser (slow) or fully simulated in Python (fast).

    Because the tests heavily rely on the `async` and `await` keywords, you should activate the `asyncio`
    [auto-mode](https://pytest-asyncio.readthedocs.io/en/latest/concepts.html#auto-mode).
    Either create a `pytest.ini` file in your project root or add it directly to your `pyproject.toml`.
    Depending on your project structure you also need a `conftest.py`, and an empty `__init__.py` to make your code a package.
''')


@doc.ui
def user_fixture():
    with ui.row(wrap=False).classes('gap-4 items-center'):
        with python_window(classes='w-[300px] h-42', title='pytest.ini'):
            ui.markdown('''
                ```ini
                [pytest]
                asyncio_mode = auto
                ```
                ''')

        ui.label('or').classes('text-2xl')

        with python_window(classes='w-[300px] h-42', title='pyproject.toml'):
            ui.markdown('''
                ```toml
                [tool.pytest.ini_options]
                asyncio_mode = "auto"
                ```
                ''')


doc.text('Simple Project Structure', '''
    For small apps and experiments you can put the tests in a separate file as we do in the examples
    [chat-app](https://github.com/zauberzeug/nicegui/tree/main/examples/chat_app) and [authentication](https://github.com/zauberzeug/nicegui/tree/main/examples/authentication).
    To properly re-init your `main.py` in the tests, you place an empty `__init__.py` file next to your code to make it a package and use the `module_under_test` marker.
    Also make sure you properly guard the `ui.run()` call in your `main.py` to prevent it from running during the tests:
''')


@doc.ui
def simple_project_code():
    with ui.row(wrap=False).classes('gap-4'):
        with python_window(classes='w-[400px] h-64'):
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

        with python_window(classes='w-[400px] h-64', title='test_app.py'):
            ui.markdown('''
                ```python
                import pytest
                from nicegui import ui
                from nicegui.testing import User
                from . import main

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


doc.text('Modular Project Structure', '''
    A more modular approach is to create a separate package for your code with an empty `__init__.py`
    and a `tests` folder for your tests.
    In your package a `startup.py` file can be used to register pages and do initialization.
    The `main.py` at root level then only imports the startup routine and calls `ui.run()`.
    An empty `conftest.py` file in the root directory makes the package with it's `startup` routine available to the tests.
''')


@doc.ui
def modular_project():
    with ui.row(wrap=False).classes('gap-4'):
        with python_window(classes='w-[400px] h-60'):
            ui.markdown('''
                ```python
                from nicegui import ui, app
                from somedemo.startup import startup

                app.on_startup(startup)

                ui.run()
                ```
                ''')

        with python_window(classes='w-[400px] h-60', title='somedemo/startup.py'):
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

    with ui.row(wrap=False).classes('gap-4'):
        with python_window(classes='w-[400px] h-68', title='tests/test_app.py'):
            ui.markdown('''
                ```python
                from nicegui import ui
                from nicegui.testing import User
                from somedemo.startup import startup

                async def test_click(user: User) -> None:
                    startup()
                    await user.open('/')
                    await user.should_see('Click me')
                    user.find(ui.button).click()
                    await user.should_see('Hello World!')
                ```
                ''')

        with bash_window(classes='w-[400px] h-42'):
            ui.markdown('''
                ```bash
                $ tree
                .
                ├── main.py
                ├── pytest.ini
                ├── somedemo
                │   ├── __init__.py
                │   └── startup.py
                └── tests
                    ├── conftest.py
                    └── test_app.py
                ```
            ''')


doc.text('', '''
    You can also create your own fixture in your `conftest.py` which calls the `startup` routine.
    Pytest has some magic to automatically find and use this specialized fixture in your tests.
    This way you can keep your tests clean and simple.
''')


@doc.ui
def custom_user_fixture():
    with ui.row(wrap=False).classes('gap-4'):
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
                from somedemo.startup import startup

                @pytest.fixture
                def user(user: User) -> User:
                    startup()
                    return user
                ```
                ''')
