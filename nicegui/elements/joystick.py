from .custom_view import CustomView
from .element import Element

class JoystickView(CustomView):

    def __init__(self, on_move):

        self.on_move = on_move

        super().__init__('joystick', __file__, [
            'https://cdn.jsdelivr.net/npm/nipplejs@0.9.0/dist/nipplejs.min.js',
        ])

        self.allowed_events = ['onMove']

        self.initialize(temp=False, onMove=self.handle_move)

    def handle_move(self, msg):

        self.on_move(msg.data)

class Joystick(Element):

    def __init__(self, *, on_move):

        super().__init__(JoystickView(on_move))
