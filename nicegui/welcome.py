import asyncio
import os
import socket
from typing import List

from . import globals  # pylint: disable=redefined-builtin

try:
    import netifaces
    globals.optional_features.add('netifaces')
except ImportError:
    pass


def get_all_ips() -> List[str]:
    if 'netifaces' not in globals.optional_features:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname_ex(hostname)[2]
        except socket.gaierror:
            return []
    ips = []
    for interface in netifaces.interfaces():  # pylint: disable=c-extension-no-member
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']  # pylint: disable=c-extension-no-member
            ips.append(ip)
        except KeyError:
            pass
    return ips


async def print_message() -> None:
    print('NiceGUI ready to go ', end='', flush=True)
    host = os.environ['NICEGUI_HOST']
    port = os.environ['NICEGUI_PORT']
    loop = asyncio.get_running_loop()
    ips = set((await loop.run_in_executor(None, get_all_ips)) if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    addresses = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost'] + sorted(ips)]
    if len(addresses) >= 2:
        addresses[-1] = 'and ' + addresses[-1]
    extra = ''
    if 'netifaces' not in globals.optional_features:
        extra = ' (install netifaces to show all IPs and speedup this message)'
    print(f'on {", ".join(addresses)}' + extra, flush=True)
