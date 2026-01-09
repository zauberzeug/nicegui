from ..context import context
from ..events import GenericEventArguments, Handler


def on_exception(handler: Handler[GenericEventArguments]):
    """Register a handler for non-critical exceptions occurring in the current page's UI context.

    :param handler: callback that is called upon occurrence of the event.

    Note: If the handler takes a parameter `e`, then:

    - the exception is in `e.args`,
    - the client is in `e.client` (same as `ui.context.client`),
    - the offending element is in `e.sender` (either `ui.context.client.content` or a `ui.sub_page`).
    """
    context.client.content.on('__error__', handler)
