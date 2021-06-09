import os.path
from .custom_view import CustomView
from .element import Element

class JoystickView(CustomView):

    vue_type = 'joystick'
    vue_filepath = os.path.realpath(__file__).replace('.py', '.js')
    vue_dependencies = [
        'https://cdn.jsdelivr.net/npm/nipplejs@0.9.0/dist/nipplejs.min.js',
    ]

    def __init__(self, on_move):

        self.on_move = on_move

        super().__init__()
        self.allowed_events = ['onMove']
        self.initialize(temp=False, onMove=self.handle_move)

    def handle_move(self, msg):

        self.on_move(msg.data)

class Joystick(Element):

    def __init__(self, *, on_move):

        super().__init__(JoystickView(on_move))
