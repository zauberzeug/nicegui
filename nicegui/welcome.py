import os
from typing import List

import ifaddr

from . import core, run


def _get_all_ips() -> List[str]:
    ips: List[str] = []
    for adapter in ifaddr.get_adapters():
        ips.extend(str(i.ip) for i in adapter.ips if i.is_IPv4)
    return ips


async def collect_urls() -> None:
    """Print a welcome message with URLs to access the NiceGUI app."""
    host = os.environ.get('NICEGUI_HOST')
    port = os.environ.get('NICEGUI_PORT')
    if not host or not port:
        return
    ips = set((await run.io_bound(_get_all_ips)) if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    urls = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost', *sorted(ips)]]
    core.app.urls.update(urls)
    if len(urls) >= 2:
        urls[-1] = 'and ' + urls[-1]
    if core.app.config.show_welcome_message:
        print(f'NiceGUI ready to go on {", ".join(urls)}', flush=True)
