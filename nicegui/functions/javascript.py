from ..awaitable_response import AwaitableResponse
from ..context import context


def run_javascript(code: str, *, timeout: float = 1.0) -> AwaitableResponse:
    """Run JavaScript

    This function runs arbitrary JavaScript code on a page that is executed in the browser.
    To access a client-side Vue component or HTML element by ID,
    use the JavaScript functions `getElement()` or `getHtmlElement()` (*added in version 2.9.0*).

    If the function is awaited, the result of the JavaScript code is returned.
    Otherwise, the JavaScript code is executed without waiting for a response.

    Obviously the JavaScript code is only executed after the client is connected.
    Internally, ``await client.connected()`` is called before the JavaScript code is executed (*since version 3.0.0*).
    This might delay the execution of the JavaScript code and is not covered by the ``timeout`` parameter.

    :param code: JavaScript code to run
    :param timeout: timeout in seconds (default: 1.0)

    :return: AwaitableResponse that can be awaited to get the result of the JavaScript code
    """
    return context.client.run_javascript(code, timeout=timeout)
