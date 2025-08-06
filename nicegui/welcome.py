import os

import ifaddr

from . import core, run


def _get_all_ips() -> list[str]:
    ips: list[str] = []
    for adapter in ifaddr.get_adapters():
        ips.extend(str(i.ip) for i in adapter.ips if i.is_IPv4)
    return ips


async def collect_urls() -> None:
    """Print a welcome message with URLs to access the NiceGUI app."""
    host = os.environ.get('NICEGUI_HOST')
    port = os.environ.get('NICEGUI_PORT')
    protocol = os.environ.get('NICEGUI_PROTOCOL')
    if not host or not port or not protocol:
        return
    ips = set((await run.io_bound(_get_all_ips)) if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    sorted_ips = ['localhost' if host == '0.0.0.0' else host, *sorted(ips)]
    urls = [(f'{protocol}://{ip}:{port}' if port != '80' else f'{protocol}://{ip}') for ip in sorted_ips]
    core.app.urls.update(urls)
    if len(urls) >= 2:
        urls[-1] = 'and ' + urls[-1]
    if core.app.config.show_welcome_message:
        print(f'NiceGUI ready to go on {", ".join(urls)}', flush=True)
