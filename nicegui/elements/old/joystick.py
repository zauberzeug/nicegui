from typing import Any, Callable, Optional

from ..routes import add_dependencies
from .custom_view import CustomView
from .element import Element

add_dependencies(__file__, ['nipplejs.min.js'])


class JoystickView(CustomView):

    def __init__(self,
                 on_start: Optional[Callable],
                 on_move: Optional[Callable],
                 on_end: Optional[Callable],
                 **options: Any):
        super().__init__('joystick', **options)

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
            return self.on_start(msg) or False
        return False

    def handle_move(self, msg):
        if self.on_move is not None:
            return self.on_move(msg) or False
        return False

    def handle_end(self, msg):
        if self.on_end is not None:
            return self.on_end(msg) or False
        return False


class Joystick(Element):

    def __init__(self, *,
                 on_start: Optional[Callable] = None,
                 on_move: Optional[Callable] = None,
                 on_end: Optional[Callable] = None,
                 **options: Any):
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user touches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """
        super().__init__(JoystickView(on_start, on_move, on_end, **options))
