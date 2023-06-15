from typing import Any, Optional

from .. import globals


async def run_javascript(code: str, *,
                         respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Optional[Any]:
    """Run JavaScript

    This function runs arbitrary JavaScript code on a page that is executed in the browser.
    The asynchronous function will return after the command(s) are executed.
    The client must be connected before this function is called.
    To access a client-side object by ID, use the JavaScript function `getElement()`.

    :param code: JavaScript code to run
    :param respond: whether to wait for a response (default: `True`)
    :param timeout: timeout in seconds (default: `1.0`)
    :param check_interval: interval in seconds to check for a response (default: `0.01`)

    :return: response from the browser, or `None` if `respond` is `False`
    """
    client = globals.get_client()
    if not client.has_socket_connection:
        raise RuntimeError(
            'Cannot run JavaScript before client is connected; try "await client.connected()" or "client.on_connect(...)".')

    return await client.run_javascript(code, respond=respond, timeout=timeout, check_interval=check_interval)
