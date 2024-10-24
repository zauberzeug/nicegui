from typing import Any, Optional

from typing_extensions import Self

from ..element import Element
from ..events import GenericEventArguments, Handler, JoystickEventArguments, handle_event


class Joystick(Element,
               component='joystick.vue',
               dependencies=['lib/nipplejs/nipplejs.js'],
               default_classes='nicegui-joystick'):

    def __init__(self, *,
                 on_start: Optional[Handler[JoystickEventArguments]] = None,
                 on_move: Optional[Handler[JoystickEventArguments]] = None,
                 on_end: Optional[Handler[JoystickEventArguments]] = None,
                 throttle: float = 0.05,
                 **options: Any) -> None:
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user touches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param throttle: throttle interval in seconds for the move event (default: 0.05)
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """
        super().__init__()
        self._props['options'] = options
        self.active = False

        self._start_handlers = [on_start] if on_start else []
        self._move_handlers = [on_move] if on_move else []
        self._end_handlers = [on_end] if on_end else []

        def handle_start() -> None:
            self.active = True
            args = JoystickEventArguments(sender=self, client=self.client, action='start')
            for handler in self._start_handlers:
                handle_event(handler, args)

        def handle_move(e: GenericEventArguments) -> None:
            if self.active:
                args = JoystickEventArguments(sender=self,
                                              client=self.client,
                                              action='move',
                                              x=float(e.args['data']['vector']['x']),
                                              y=float(e.args['data']['vector']['y']))
                for handler in self._move_handlers:
                    handle_event(handler, args)

        def handle_end() -> None:
            self.active = False
            args = JoystickEventArguments(sender=self,
                                          client=self.client,
                                          action='end')
            for handler in self._end_handlers:
                handle_event(handler, args)

        self.on('start', handle_start, [])
        self.on('move', handle_move, ['data'], throttle=throttle)
        self.on('end', handle_end, [])

    def on_start(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user touches the joystick."""
        self._start_handlers.append(callback)
        return self

    def on_move(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user moves the joystick."""
        self._move_handlers.append(callback)
        return self

    def on_end(self, callback: Handler[JoystickEventArguments]) -> Self:
        """Add a callback to be invoked when the user releases the joystick."""
        self._end_handlers.append(callback)
        return self
