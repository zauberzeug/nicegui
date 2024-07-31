from nicegui.testing import User
from . import doc
from nicegui import ui
from ..windows import python_window


@doc.part('User Fixture')
def user_fixture():
    ui.markdown('''
        We recommend you utilize the `user` fixture instead of the [`screen` fixture](/documentation/screen) wherever possible because execution is as fast as unit tests and it does not need Selenium as a dependency.
        The `user` fixture cuts away the browser and replaces it by a light weight simulation which entirely runs in Python.

        You can assert for specific elements or content, click buttons, type into inputs and trigger events.
        We aimed for a nice API to write acceptance tests which read like a story and are easy to understand.
        Due to the fast execution, the classical [test pyramid](https://martinfowler.com/bliki/TestPyramid.html)
        where UI tests are considered slow and expensive does not apply anymore.
        ''')

    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            await user.open('/')
            user.find('Username').type('user1')
            user.find('Password').type('pass1').trigger('keydown.enter')
            await user.should_see('Hello user1!')
            user.find('logout').click()
            await user.should_see('Log in')
            ```''')


doc.text('Querying', '''
    The querying capabilities of the `User` are build upon the [ElementFilter](/documentation/element_filter).
    So in a similar fashion the `.should_see(...)` method and `.find(...)`method provide parameters to filter for
    content, [markers](/documentation/element_filter#markers), types, etc.
    If you do not provide a named property, the string will be matched against the text content and markers.
''')


@doc.ui
def modular_project():
    with ui.row(wrap=False).classes('gap-4'):
        with python_window(classes='w-[400px] h-48', title='some ui code'):
            ui.markdown('''
                ```python
                with ui.row():
                    ui.label('Hello World!').mark('greeting')
                    ui.icon('star')
                with ui.row():
                    ui.label('Hello Universe!')
                    ui.input(placeholder='Type here')
                ```''')

        with python_window(classes='w-[600px] h-48', title='user assertions'):
            ui.markdown('''
                ```python
                await user.should_see('greeting')
                await user.should_see('star')
                await user.should_see('Hello Universe!')
                await user.should_see('Type here')
                await user.should_see('Hello')
                await user.should_see('Hello', marker='greeting')
                await user.should_see('Hello', marker='greeting', kind=ui.label)
                ```
                ''')


doc.text('Comparison with the screen fixture', '''
    By cutting out the browser, test execution becomes much faster than the [`screen` fixture](/documentation/screen).
    Of course some features like screenshots or browser specific behavior are not available.
    See our [pytests example](https://github.com/zauberzeug/nicegui/tree/main/examples/pytests) which implements the same tests with both fixtures.
''')

doc.reference(User)
