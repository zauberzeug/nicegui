from typing import Optional, Union

from .. import background_tasks, globals


def notify(message: str, *,
           position: str = 'bottom',
           closeBtn: Union[bool, str] = False,
           type: Optional[str] = None,
           color: Optional[str] = None,
           **kwargs,
           ) -> None:
    """Notification

    Displays a notification on the screen.

    :param message: content of the notification
    :param position: position on the screen ("top-left", "top-right", "bottom-left", "bottom-right, "top", "bottom", "left", "right" or "center", default: "bottom")
    :param closeBtn: optional label of a button to dismiss the notification (default: `False`)
    :param type: optional type ("positive", "negative", "warning", "info" or "ongoing")
    :param color: optional color name

    Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
    """
    options = {key: value for key, value in locals().items() if not key.startswith('_') and value is not None}
    background_tasks.create(globals.sio.emit('notify', options, room=globals.get_client().id))
