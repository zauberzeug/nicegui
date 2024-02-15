import os
from typing import List

import ifaddr

from . import core, run


def _get_all_ips() -> List[str]:
    """
    Get a list of all IPv4 addresses associated with the network adapters.

    Returns:
        List[str]: A list of IPv4 addresses.

    """
    ips: List[str] = []
    for adapter in ifaddr.get_adapters():
        ips.extend(str(i.ip) for i in adapter.ips if i.is_IPv4)
    return ips


async def collect_urls() -> None:
    """Collects URLs to access the NiceGUI app and updates the app's URL list.

    This function collects the URLs that can be used to access the NiceGUI app based on the host and port
    environment variables. It then updates the app's URL list with the collected URLs.

    The function first checks if the 'NICEGUI_HOST' and 'NICEGUI_PORT' environment variables are set. If
    either of them is missing, the function returns without performing any further actions.

    If both 'NICEGUI_HOST' and 'NICEGUI_PORT' are present, the function proceeds to collect the IP addresses
    associated with the host. If the host is set to '0.0.0.0', it retrieves all IP addresses associated with
    the system. Otherwise, it retrieves an empty list.

    The function discards the '127.0.0.1' IP address from the collected IPs and constructs a list of URLs
    using the collected IPs and the port. If the port is set to '80', it omits the port number from the URLs.

    The function then updates the app's URL list with the constructed URLs using the `core.app.urls.update()`
    method.

    If there are at least two URLs in the list, the last URL is modified to include the word 'and' before it.

    Finally, if the 'show_welcome_message' configuration option is enabled, the function prints a welcome
    message to the console, indicating the URLs that can be used to access the NiceGUI app.

    Note: This function assumes that the NiceGUI app is running in an asynchronous context.

    Usage:
        - Ensure that the 'NICEGUI_HOST' and 'NICEGUI_PORT' environment variables are set.
        - Call the `collect_urls()` function to collect and update the app's URL list.
        - Optionally, check the 'show_welcome_message' configuration option to determine if the welcome
          message should be printed.

    Raises:
        None
    """
    host = os.environ.get('NICEGUI_HOST')
    port = os.environ.get('NICEGUI_PORT')
    if not host or not port:
        return
    ips = set((await run.io_bound(_get_all_ips)) if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    urls = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost'] + sorted(ips)]
    core.app.urls.update(urls)
    if len(urls) >= 2:
        urls[-1] = 'and ' + urls[-1]
    if core.app.config.show_welcome_message:
        print(f'NiceGUI ready to go on {", ".join(urls)}', flush=True)
