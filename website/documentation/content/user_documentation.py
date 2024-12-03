from nicegui import ui
from nicegui.testing import User, UserInteraction

from ..windows import python_window
from . import doc


@doc.part('User Fixture')
def user_fixture():
    ui.markdown('''
        We recommend utilizing the `user` fixture instead of the [`screen` fixture](/documentation/screen) wherever possible
        because execution is as fast as unit tests and it does not need Selenium as a dependency
        when loaded via `pytest_plugins = ['nicegui.testing.user_plugin']`.
        The `user` fixture cuts away the browser and replaces it by a lightweight simulation entirely in Python.
        See [project structure](/documentation/project_structure) for a description of the setup.

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
def querying():
    with ui.row().classes('gap-4 items-stretch'):
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


doc.text('Complex elements', '''
    There are some elements with complex visualization and interaction behaviors (`ui.upload`, `ui.table`, ...).
    Not every aspect of these elements can be tested with `should_see` and `UserInteraction`.
    Still, you can grab them with `user.find(...)` and do the testing on the elements themselves.
''')


@doc.ui
def upload_table():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                def receive_file(e: events.UploadEventArguments):
                    content = e.content.read().decode('utf-8')
                    reader = csv.DictReader(content.splitlines())
                    ui.table(
                        columns=[{
                            'name': h,
                            'label': h.capitalize(),
                            'field': h,
                        } for h in reader.fieldnames or []],
                        rows=list(reader),
                    )

                ui.upload(on_upload=receive_file)
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                upload = user.find(ui.upload).elements.pop()
                upload.handle_uploads([UploadFile(
                    BytesIO(b'name,age\\nAlice,30\\nBob,28'),
                    filename='data.csv',
                    headers=Headers(raw=[(b'content-type', b'text/csv')]),
                )])
                table = user.find(ui.table).elements.pop()
                assert table.columns == [
                    {'name': 'name', 'label': 'Name', 'field': 'name'},
                    {'name': 'age', 'label': 'Age', 'field': 'age'},
                ]
                assert table.rows == [
                    {'name': 'Alice', 'age': '30'},
                    {'name': 'Bob', 'age': '28'},
                ]
                ```
            ''')


doc.text('Autocomplete', '''
    The `UserInteraction` object returned by `user.find(...)` provides methods to trigger events on the found elements.
    This demo shows how to trigger a "keydown.tab" event to autocomplete an input field.
''')


@doc.ui
def trigger_events():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                fruits = ['apple', 'banana', 'cherry']
                ui.input(label='fruit', autocomplete=fruits)
                ```
            ''')
        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.open('/')
                user.find('fruit').type('a').trigger('keydown.tab')
                await user.should_see('apple')
                ```
            ''')


doc.text('Test Downloads', '''
    You can verify that a download was triggered by checking `user.downloads.http_responses`.
    By awaiting `user.downloads.next()` you can get the next download response.
''')


@doc.ui
def check_outbox():
    with ui.row().classes('gap-4 items-stretch'):
        with python_window(classes='w-[500px]', title='some UI code'):
            ui.markdown('''
                ```python
                @ui.page('/')
                def page():
                    def download():
                        ui.download(b'Hello', filename='hello.txt')

                    ui.button('Download', on_click=download)
                ```
            ''')

        with python_window(classes='w-[500px]', title='user assertions'):
            ui.markdown('''
                ```python
                await user.open('/')
                assert len(user.download.http_responses) == 0
                user.find('Download').click()
                response = await user.download.next()
                assert response.text == 'Hello'
                ```
            ''')


doc.text('Multiple Users', '''
    Sometimes it is not enough to just interact with the UI as a single user.
    Besides the `user` fixture, we also provide the `create_user` fixture which is a factory function to create users.
    The `User` instances are independent from each other and can interact with the UI in parallel.
    See our [Chat App example](https://github.com/zauberzeug/nicegui/blob/main/examples/chat_app/test_chat_app.py)
    for a full demonstration.
''')


@doc.ui
def multiple_users():
    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            async def test_chat(create_user: Callable[[], User]) -> None:
                userA = create_user()
                await userA.open('/')
                userB = create_user()
                await userB.open('/')

                userA.find(ui.input).type('from A').trigger('keydown.enter')
                await userB.should_see('from A')
                userB.find(ui.input).type('from B').trigger('keydown.enter')
                await userA.should_see('from A')
                await userA.should_see('from B')
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
