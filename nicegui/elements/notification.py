from typing import Any, Literal, Optional, Union

from ..context import context
from ..element import Element
from .timer import Timer

NotificationPosition = Literal[
    'top-left',
    'top-right',
    'bottom-left',
    'bottom-right',
    'top',
    'bottom',
    'left',
    'right',
    'center',
]

NotificationType = Optional[Literal[
    'positive',
    'negative',
    'warning',
    'info',
    'ongoing',
]]


class Notification(Element, component='notification.js'):

    def __init__(self,
                 message: Any = '', *,
                 position: NotificationPosition = 'bottom',
                 close_button: Union[bool, str] = False,
                 type: NotificationType = None,  # pylint: disable=redefined-builtin
                 color: Optional[str] = None,
                 multi_line: bool = False,
                 icon: Optional[str] = None,
                 spinner: bool = False,
                 timeout: Optional[float] = 5.0,
                 **kwargs: Any,
                 ) -> None:
        """Notification element

        Displays a notification on the screen.
        In contrast to `ui.notify`, this element allows to update the notification message and other properties once the notification is displayed.
        The notification can be removed with `dismiss()`.

        :param message: content of the notification
        :param position: position on the screen ("top-left", "top-right", "bottom-left", "bottom-right", "top", "bottom", "left", "right" or "center", default: "bottom")
        :param close_button: optional label of a button to dismiss the notification (default: `False`)
        :param type: optional type ("positive", "negative", "warning", "info" or "ongoing")
        :param color: optional color name
        :param multi_line: enable multi-line notifications
        :param icon: optional name of an icon to be displayed in the notification (default: `None`)
        :param spinner: display a spinner in the notification (default: False)
        :param timeout: optional timeout in seconds after which the notification is dismissed (default: 5.0)

        Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
        """
        with context.client.layout:
            super().__init__()
        self._props['options'] = {
            'message': str(message),
            'position': position,
            'multiLine': multi_line,
            'spinner': spinner,
            'closeBtn': close_button,
            'timeout': (timeout or 0) * 1000,
            'group': False,
            'attrs': {'data-id': f'nicegui-dialog-{self.id}'},
        }
        if type is not None:
            self._props['options']['type'] = type
        if color is not None:
            self._props['options']['color'] = color
        if icon is not None:
            self._props['options']['icon'] = icon
        self._props['options'].update(kwargs)
        with self:
            def delete():
                self.clear()
                self.delete()

            async def try_delete():
                query = f'''!!document.querySelector("[data-id='nicegui-dialog-{self.id}']")'''
                if not await self.client.run_javascript(query):
                    delete()

            Timer(1.0, try_delete)

    @property
    def message(self) -> str:
        """Message text."""
        return self._props['options']['message']

    @message.setter
    def message(self, value: Any) -> None:
        self._props['options']['message'] = str(value)
        self.update()

    @property
    def position(self) -> NotificationPosition:
        """Position on the screen."""
        return self._props['options']['position']

    @position.setter
    def position(self, value: NotificationPosition) -> None:
        self._props['options']['position'] = value
        self.update()

    @property
    def type(self) -> NotificationType:
        """Type of the notification."""
        return self._props['options'].get('type')

    @type.setter
    def type(self, value: NotificationType) -> None:
        if value is None:
            self._props['options'].pop('type', None)
        else:
            self._props['options']['type'] = value
        self.update()

    @property
    def color(self) -> Optional[str]:
        """Color of the notification."""
        return self._props['options'].get('color')

    @color.setter
    def color(self, value: Optional[str]) -> None:
        if value is None:
            self._props['options'].pop('color', None)
        else:
            self._props['options']['color'] = value
        self.update()

    @property
    def multi_line(self) -> bool:
        """Whether the notification is multi-line."""
        return self._props['options']['multiLine']

    @multi_line.setter
    def multi_line(self, value: bool) -> None:
        self._props['options']['multiLine'] = value
        self.update()

    @property
    def icon(self) -> Optional[str]:
        """Icon of the notification."""
        return self._props['options'].get('icon')

    @icon.setter
    def icon(self, value: Optional[str]) -> None:
        if value is None:
            self._props['options'].pop('icon', None)
        else:
            self._props['options']['icon'] = value
        self.update()

    @property
    def spinner(self) -> bool:
        """Whether the notification is a spinner."""
        return self._props['options']['spinner']

    @spinner.setter
    def spinner(self, value: bool) -> None:
        self._props['options']['spinner'] = value
        self.update()

    @property
    def close_button(self) -> Union[bool, str]:
        """Whether the notification has a close button."""
        return self._props['options']['closeBtn']

    @close_button.setter
    def close_button(self, value: Union[bool, str]) -> None:
        self._props['options']['closeBtn'] = value
        self.update()

    def dismiss(self) -> None:
        """Dismiss the notification."""
        self.run_method('dismiss')
