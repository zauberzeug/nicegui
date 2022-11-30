from typing import Optional

from .. import globals


async def run_javascript(code: str, *,
                         respond: bool = True, timeout: float = 1.0, check_interval: float = 0.01) -> Optional[str]:
    client = globals.get_client()
    if not client.has_socket_connection:
        raise RuntimeError('Cannot run JavaScript before client handshake.')

    return await client.run_javascript(code, respond=respond, timeout=timeout, check_interval=check_interval)
