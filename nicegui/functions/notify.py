from typing import Any, Literal

from ..context import context

ARG_MAP = {
    'close_button': 'closeBtn',
    'multi_line': 'multiLine',
}


# pylint: disable=unused-argument
def notify(message: Any, *,
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
           close_button: bool | str = False,
           type: Literal[  # pylint: disable=redefined-builtin
               'positive',
               'negative',
               'warning',
               'info',
               'ongoing',
           ] | None = None,
           color: str | None = None,
           multi_line: bool = False,
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

    Note: You can pass additional keyword arguments according to `Quasar's Notify API <https://quasar.dev/quasar-plugins/notify#notify-api>`_.
    """
    options = {ARG_MAP.get(key, key): value for key, value in locals().items() if key != 'kwargs' and value is not None}
    options['message'] = str(message)
    options.update(kwargs)
    client = context.client
    client.outbox.enqueue_message('notify', options, client.id)
