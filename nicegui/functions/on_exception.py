from ..context import context
from ..events import GenericEventArguments, Handler


def on_exception(handler: Handler[GenericEventArguments]):
    """Register a handler for non-critical exceptions occurring in the current page's UI context."""
    context.client.content.on('__error__', handler)
