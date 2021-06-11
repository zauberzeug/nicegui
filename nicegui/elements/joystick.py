from .custom_view import CustomView
from .element import Element

class JoystickView(CustomView):

    def __init__(self, on_start, on_move, on_end, **options):

        super().__init__('joystick', __file__, [
            'https://cdn.jsdelivr.net/npm/nipplejs@0.9.0/dist/nipplejs.min.js',
        ], **options)

        self.on_start = on_start
        self.on_move = on_move
        self.on_end = on_end
        self.allowed_events = ['onStart', 'onMove', 'onEnd']
        self.initialize(temp=False,
                        onStart=self.handle_start,
                        onMove=self.handle_move,
                        onEnd=self.handle_end)

    def handle_start(self, msg):

        if self.on_start is not None:
            self.on_start(msg)

    def handle_move(self, msg):

        if self.on_move is not None:
            self.on_move(msg)

    def handle_end(self, msg):

        if self.on_end is not None:
            self.on_end(msg)

class Joystick(Element):

    def __init__(self, *, on_start=None, on_move=None, on_end=None, **options):

        super().__init__(JoystickView(on_start, on_move, on_end, **options))
