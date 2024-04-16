from typing import Optional

from ..awaitable_response import AwaitableResponse
from ..context import context


def run_javascript(code: str, *,
                   respond: Optional[bool] = None,
                   timeout: float = 1.0, check_interval: float = 0.01) -> AwaitableResponse:
    """Run JavaScript

    This function runs arbitrary JavaScript code on a page that is executed in the browser.
    The client must be connected before this function is called.
    To access a client-side object by ID, use the JavaScript function `getElement()`.

    If the function is awaited, the result of the JavaScript code is returned.
    Otherwise, the JavaScript code is executed without waiting for a response.

    :param code: JavaScript code to run
    :param timeout: timeout in seconds (default: `1.0`)

    :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
    """
    return context.client.run_javascript(code, respond=respond, timeout=timeout, check_interval=check_interval)
