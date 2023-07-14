import os
import socket
from typing import List

from .globals import optional_features

try:
    import netifaces
    optional_features.append('netifaces')
except ImportError:
    pass


def get_all_ips() -> List[str]:
    if not 'netifaces' in optional_features:
        return [info[4][0] for info in socket.getaddrinfo(socket.gethostname(), None) if len(info[4]) == 2]
    ips = []
    for interface in netifaces.interfaces():
        try:
            ips.append(netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'])
        except KeyError:
            pass
    return ips


def print_message() -> None:
    host = os.environ['NICEGUI_HOST']
    port = os.environ['NICEGUI_PORT']
    ips = set(get_all_ips() if host == '0.0.0.0' else [])
    ips.discard('127.0.0.1')
    addresses = [(f'http://{ip}:{port}' if port != '80' else f'http://{ip}') for ip in ['localhost'] + sorted(ips)]
    if len(addresses) >= 2:
        addresses[-1] = 'and ' + addresses[-1]
    print(f'NiceGUI ready to go on {", ".join(addresses)}', flush=True)
