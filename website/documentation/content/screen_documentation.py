from nicegui.testing import Screen
from . import doc
from nicegui.testing import Screen
from ..windows import python_window
from nicegui import ui


@doc.part('Screen Fixture')
def screen_fixture():

    ui.markdown('''
    The `screen` fixture starts a real (headless) browser to interact with your application.
    This is only necessary if you have browser specific behavior to test.
    NiceGUI itself is thoroughly tested with this fixture to ensure each component works as expected.
    So only use it if you have to.
''')

    with python_window(classes='w-[600px]', title='example'):
        ui.markdown('''
            ```python
            from selenium.webdriver.common.keys import Keys

            screen.open('/')
            screen.type(Keys.TAB) # to focus on the first input
            screen.type('user1')
            screen.type(Keys.TAB) # to focus the second input
            screen.type('pass1')
            screen.click('Log in')
            screen.should_contain('Hello user1!')
            screen.click('logout')
            screen.should_contain('Log in')
            ```''')


doc.reference(Screen)
