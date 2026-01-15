from typing import Callable

from ..context import context


def on_exception(handler: Callable):
    """Register a handler for non-critical exceptions occurring in the current page's UI context.

    :param handler: callback that is called upon occurrence of the event.

    Note: If the handler takes a parameter `e`, then:

    - the exception is in `e.args`,
    - the client is in `e.client` (same as `ui.context.client`),
    - the offending element is in `e.sender` (either `ui.context.client.content` or a `ui.sub_page`).
    """
    context.client.on_exception(handler)
