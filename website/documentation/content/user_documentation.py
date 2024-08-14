from nicegui import ui
from nicegui.testing import User, UserInteraction

from ..windows import python_window
from . import doc


@doc.part('User Fixture')
def user_fixture():
    ui.markdown('''
        We recommend utilizing the `user` fixture instead of the [`screen` fixture](/documentation/screen) wherever possible
        because execution is as fast as unit tests and it does not need Selenium as a dependency
        when loaded via `pytest_plugins = ['nicegui.testing.user_plugin']` (see [project structure](/documentation/project_structure)).
        The `user` fixture cuts away the browser and replaces it by a lightweight simulation entirely in Python.

        You can assert to "see" specific elements or content, click buttons, type into inputs and trigger events.
        We aimed for a nice API to write acceptance tests which read like a story and are easy to understand.
        Due to the fast execution, the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html),
        where UI tests are considered slow and expensive, does not apply anymore.
    ''').classes('bold-links arrow-links')

    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            await user.open('/')
            user.find('Username').type('user1')
            user.find('Password').type('pass1').trigger('keydown.enter')
            await user.should_see('Hello user1!')
            user.find('logout').click()
            await user.should_see('Log in')
            ```
        ''')

    ui.markdown('''
        **NOTE:** The `user` fixture is quite new and still misses some features.
        Please let us know in separate feature requests
        [over on GitHub](https://github.com/zauberzeug/nicegui/discussions/new?category=ideas-feature-requests).
    ''').classes('bold-links arrow-links')


@doc.part('Async execution')
def async_execution():
    ui.markdown('''
        The user simulation runs in the same async context as your app
        to make querying and interaction as easy as possible.
        But that also means that your tests must be `async`.
        We suggest to activate the [pytest-asyncio auto-mode](https://pytest-asyncio.readthedocs.io/en/latest/concepts.html#auto-mode)
        by either creating a `pytest.ini` file in your project root
        or adding the activation directly to your `pyproject.toml`.
    ''').classes('bold-links arrow-links')

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


doc.text('Querying', '''
    The querying capabilities of the `User` are built upon the [ElementFilter](/documentation/element_filter).
    The `user.should_see(...)` method and `user.find(...)` method
    provide parameters to filter for content, [markers](/documentation/element_filter#markers), types, etc.
    If you do not provide a named property, the string will match against the text content and markers.
''')


@doc.ui
def modular_project():
    with ui.row(wrap=False).classes('gap-4 items-stretch'):
        with python_window(classes='w-[400px]', title='some UI code'):
            ui.markdown('''
                ```python
                with ui.row():
                    ui.label('Hello World!').mark('greeting')
                    ui.icon('star')
                with ui.row():
                    ui.label('Hello Universe!')
                    ui.input(placeholder='Type here')
                ```
            ''')

        with python_window(classes='w-[600px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.should_see('greeting')
                await user.should_see('star')
                await user.should_see('Hello Universe!')
                await user.should_see('Type here')
                await user.should_see('Hello')
                await user.should_see(marker='greeting')
                await user.should_see(kind=ui.icon)
                ```
            ''')


doc.text('Comparison with the screen fixture', '''
    By cutting out the browser, test execution becomes much faster than the [`screen` fixture](/documentation/screen).
    Of course, some features like screenshots or browser-specific behavior are not available.
    See our [pytests example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests)
    which implements the same tests with both fixtures.
''')

doc.reference(User, title='User Reference')
doc.reference(UserInteraction, title='UserInteraction Reference')
