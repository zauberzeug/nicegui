from nicegui.testing import Screen
from . import doc

doc.text('Screen Fixture', '''
    The `screen` fixture starts a real(headless) browser to interact with your application.
    This is only necessary if you have browser specific behavior to test.
    NiceGUI itself is thoroughly tested with this fixture to ensure each component works as expected.
    So only use it if you have to.
''')

doc.reference(Screen)
