from typing import Any, Optional, Union

from typing_extensions import Literal

from .. import globals, outbox


def notify(message: Any, *,
           position: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top', 'bottom', 'left', 'right', 'center'] = 'bottom',
           closeBtn: Union[bool, str] = False,
           type: Optional[Literal['positive', 'negative', 'warning', 'info', 'ongoing']] = None,
           color: Optional[str] = None,
           **kwargs: Any,
           ) -> None:
    """Notification

    Displays a notification on the screen.

    :param message: content of the notification
    :param position: position on the screen ("top-left", "top-right", "bottom-left", "bottom-right", "top", "bottom", "left", "right" or "center", default: "bottom")
    :param closeBtn: optional label of a button to dismiss the notification (default: `False`)
    :param type: optional type ("positive", "negative", "warning", "info" or "ongoing")
    :param color: optional color name

    Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
    """
    options = {key: value for key, value in locals().items() if not key.startswith('_') and value is not None}
    options['message'] = str(message)
    options.update(kwargs)
    outbox.enqueue_message('notify', options, globals.get_client().id)
