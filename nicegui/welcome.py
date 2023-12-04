import os
from typing import List

import ifaddr

from . import core, run


def _get_all_ips() -> List[str]:
    ips: List[str] = []
    for adapter in ifaddr.get_adapters():
        ips.extend(str(i.ip) for i in adapter.ips if i.is_IPv4)
    return ips


async def print_message() -> None:
    """Print a welcome message with URLs to access the NiceGUI app."""
    print('NiceGUI ready to go ', end='', flush=True)
    host = os.environ['NICEGUI_HOST']
    port = os.environ['NICEGUI_PORT']
    ips = set((await run.io_bound(_get_all_ips)) if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    urls = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost'] + sorted(ips)]
    core.app.urls.update(urls)
    if len(urls) >= 2:
        urls[-1] = 'and ' + urls[-1]
    print(f'on {", ".join(urls)}', flush=True)
