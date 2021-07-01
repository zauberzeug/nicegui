from typing import Callable, Dict
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

    def __init__(self,
                 *,
                 on_start: Callable = None,
                 on_move: Callable = None,
                 on_end: Callable = None,
                 **options: Dict,
                 ):
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user toches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """

        super().__init__(JoystickView(on_start, on_move, on_end, **options))
