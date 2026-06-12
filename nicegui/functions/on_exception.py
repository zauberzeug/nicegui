from collections.abc import Callable
from typing import Any

from ..context import context


def on_exception(handler: Callable[[Exception], Any] | Callable[[], Any]) -> None:
    """Register a handler for in-page exceptions (after the page has been sent to the browser).

    The callback has an optional parameter of ``Exception``.

    *Added in version 3.6.0*

    :param handler: callback that is called upon occurrence of the event.
    """
    context.client.on_exception(handler)
