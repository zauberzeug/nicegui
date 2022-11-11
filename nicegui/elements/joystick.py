from typing import Any, Callable, Optional

from .. import vue
from ..element import Element

vue.register_component('joystick', __file__, 'joystick.vue', ['lib/nipplejs.min.js'])


class Joystick(Element):

    def __init__(self, *,
                 on_start: Optional[Callable] = None,
                 on_move: Optional[Callable] = None,
                 on_end: Optional[Callable] = None,
                 **options: Any) -> None:
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user touches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """
        super().__init__('joystick')
        self.on('start', on_start)
        self.on('move', on_move, args=['data'])
        self.on('end', on_end)
        self._props['options'] = options
