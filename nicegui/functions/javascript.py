from ..awaitable_response import AwaitableResponse
from ..context import context


def run_javascript(code: str, *, timeout: float = 1.0) -> AwaitableResponse:
    """Run JavaScript

    This function runs arbitrary JavaScript code on a page that is executed in the browser.
    The client must be connected before this function is called.
    To access a client-side Vue component or HTML element by ID,
    use the JavaScript functions `getElement()` or `getHtmlElement()`.

    If the function is awaited, the result of the JavaScript code is returned.
    Otherwise, the JavaScript code is executed without waiting for a response.

    Note that requesting data from the client is only supported for page functions, not for the shared auto-index page.

    :param code: JavaScript code to run
    :param timeout: timeout in seconds (default: `1.0`)

    :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
    """
    return context.client.run_javascript(code, timeout=timeout)
