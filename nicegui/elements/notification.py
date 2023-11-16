from typing import Any, Literal, Optional, Union

from .. import context
from ..element import Element
from .timer import Timer


class Notification(Element, component='notification.js'):

    def __init__(self,
                 message: Any, *,
                 position: Literal[
                     'top-left',
                     'top-right',
                     'bottom-left',
                     'bottom-right',
                     'top',
                     'bottom',
                     'left',
                     'right',
                     'center',
                 ] = 'bottom',
                 close_button: Union[bool, str] = False,
                 type: Optional[Literal[  # pylint: disable=redefined-builtin
                     'positive',
                     'negative',
                     'warning',
                     'info',
                     'ongoing',
                 ]] = None,
                 color: Optional[str] = None,
                 multi_line: bool = False,
                 timeout: float = 5.0,
                 **kwargs: Any,
                 ) -> None:
        """Notification

        Displays a notification on the screen.

        :param message: content of the notification
        :param position: position on the screen ("top-left", "top-right", "bottom-left", "bottom-right", "top", "bottom", "left", "right" or "center", default: "bottom")
        :param close_button: optional label of a button to dismiss the notification (default: `False`)
        :param type: optional type ("positive", "negative", "warning", "info" or "ongoing")
        :param color: optional color name
        :param multi_line: enable multi-line notifications
        :param timeout: optional timeout in seconds after which the notification is dismissed (default: 5.0)

        Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
        """
        with context.get_client().layout:
            super().__init__()
        self._props['options'] = {
            'message': str(message),
            'position': position,
            'type': type,
            'color': color,
            'multiLine': multi_line,
            'closeBtn': close_button,
            'timeout': timeout * 1000,
        }
        self._props['options'].update(kwargs)
        with self:
            def delete():
                self.clear()
                self.delete()
            Timer(timeout, delete, once=True)
