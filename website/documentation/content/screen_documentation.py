from nicegui import ui
from nicegui.testing import Screen

from ..windows import python_window
from . import doc


@doc.part('Screen Fixture')
def screen_fixture():
    ui.markdown('''
        The `screen` fixture starts a real (headless) browser to interact with your application.
        This is only necessary if you have browser-specific behavior to test.
        NiceGUI itself is thoroughly tested with this fixture to ensure each component works as expected.
        So only use it if you have to.
    ''').classes('bold-links arrow-links')

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
            ```
        ''')


@doc.part('Web driver')
def web_driver():
    ui.markdown('''
        The `screen` fixture uses Selenium under the hood.
        Currently it is only tested with the Chrome driver.
        To automatically use it for the tests we suggest to add the option `--driver Chrome` to your `pytest.ini`:
    ''').classes('bold-links arrow-links')

    with python_window(classes='w-[600px] h-42', title='pytest.ini'):
        ui.markdown('''
            ```ini
            [pytest]
            asyncio_mode = auto
            addopts = "--driver Chrome"
            ```
        ''')


doc.reference(Screen)
