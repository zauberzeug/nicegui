"""Runtime diagnostics for NiceGUI applications."""
import asyncio
import collections
import contextlib
import datetime
import sys
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from . import background_tasks, core
from .client import Client

# NOTE: resource module is POSIX-only; gracefully degrade on other platforms
try:
    import resource
except ImportError:
    resource = None  # type: ignore[assignment]


def _collect_task_summary() -> dict[str, Any]:
    """Collect asyncio task summary grouped by coroutine name."""
    tasks = asyncio.all_tasks()
    counter: collections.Counter[str] = collections.Counter()
    names_by_group: dict[str, list[str]] = {}
    for task in tasks:
        qualname = getattr(task.get_coro(), '__qualname__', '')
        # NOTE: extract last two dotted segments for readable grouping
        key = '.'.join(qualname.rsplit('.', 2)[-2:])
        counter[key] += 1
        names_by_group.setdefault(key, []).append(task.get_name())
    by_coroutine = {
        key: {'count': count, 'names': names_by_group[key]}
        for key, count in counter.most_common()
    }
    return {
        'total': len(tasks),
        'by_coroutine': by_coroutine,
    }


def _collect_memory() -> dict[str, Any]:
    """Collect memory usage metrics with source labels."""
    if resource is not None:
        peak_rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # NOTE: on Linux, ru_maxrss is in KB; on macOS it is in bytes
        peak_rss_bytes = peak_rss_raw * 1024 if sys.platform == 'linux' else peak_rss_raw
        peak_rss_source = 'resource.getrusage(RUSAGE_SELF).ru_maxrss'
    else:
        peak_rss_bytes = None
        peak_rss_source = 'resource module not available (non-POSIX platform)'

    current_rss_bytes = None
    current_rss_source = '/proc/self/status not available (non-Linux platform)'
    with contextlib.suppress(OSError):
        with open('/proc/self/status', encoding='utf-8') as f:
            for line in f:
                if line.startswith('VmRSS:'):
                    # NOTE: VmRSS line format is "VmRSS:    <number> kB"
                    current_rss_bytes = int(line.split()[1]) * 1024
                    current_rss_source = '/proc/self/status VmRSS'
                    break

    return {
        'peak_rss_bytes': peak_rss_bytes,
        'peak_rss_source': peak_rss_source,
        'current_rss_bytes': current_rss_bytes,
        'current_rss_source': current_rss_source,
    }


def _collect_client_detail(client_id: str) -> dict[str, Any]:
    """Collect detail for a specific client."""
    client = Client.instances.get(client_id)
    if client is None:
        return {'client': None, 'client_error': 'not found'}
    return {
        'client': {
            'id': client_id,
            'elements': len(client.elements),
            'outbox_pending_updates': len(client.outbox.updates),
            'outbox_pending_messages': len(client.outbox.messages),
            'has_socket_connection': client.has_socket_connection,
        },
    }


def _collect_config() -> dict[str, Any]:
    """Collect server configuration relevant to event handling and debugging."""
    # NOTE: core.sio.eio is a third-party internal; guard against attribute changes
    eio = getattr(core.sio, 'eio', None)
    config: dict[str, Any] = {
        'async_handlers': getattr(core.sio, 'async_handlers', None),
        'transports': getattr(eio, 'transports', []) if eio is not None else [],
        'reconnect_timeout': getattr(core.app.config, 'reconnect_timeout', None),
        'binding_refresh_interval': getattr(core.app.config, 'binding_refresh_interval', None),
    }
    return config


def collect_snapshot(*, client_id: str | None = None, verbose: bool = False) -> dict[str, Any]:
    """Collect a diagnostics snapshot of the running NiceGUI application."""
    result: dict[str, Any] = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'server': {
            'asyncio_tasks': _collect_task_summary(),
            'background_tasks': len(background_tasks.running_tasks),
            'memory': _collect_memory(),
            'config': _collect_config(),
            'clients_total': len(Client.instances),
            'clients_connected': sum(1 for c in Client.instances.values() if c.has_socket_connection),
        },
        'client': None,
    }

    if client_id is not None:
        result.update(_collect_client_detail(client_id))

    if verbose:
        result['clients_detail'] = [
            {
                'id': cid,
                'elements': len(c.elements),
                'has_socket_connection': c.has_socket_connection,
            }
            for cid, c in Client.instances.items()
        ]

    return result


async def get_diagnostics(request: Request) -> JSONResponse:
    """Return a JSON response with current diagnostics data.

    NOTE: must be async so Starlette runs it in the event loop, not a threadpool;
    collect_snapshot() calls asyncio.all_tasks() which requires a running loop.
    """
    client_id = request.query_params.get('client_id')
    verbose = request.query_params.get('verbose', '').lower() in ('true', '1', 'yes')
    return JSONResponse(collect_snapshot(client_id=client_id, verbose=verbose))
