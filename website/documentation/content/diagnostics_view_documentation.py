from nicegui import ui

from . import doc


@doc.demo(ui.diagnostics_view)
def main_demo() -> None:
    ui.diagnostics_view()


@doc.demo('Diagnostics Endpoint', '''
    Passing ``diagnostics=True`` to ``ui.run()`` registers a JSON endpoint at ``/_nicegui/diagnostics``.
    The endpoint returns a snapshot including:

    - ``asyncio_tasks``: total count and breakdown by coroutine name, useful for detecting task leaks
    - ``background_tasks``: count of tasks managed by ``background_tasks.create()``
    - ``memory``: current RSS (from ``/proc/self/status`` on Linux) and peak RSS (from ``resource.getrusage``),
      with source labels indicating where each value came from
    - ``config``: server settings like ``async_handlers``, ``transports``, ``reconnect_timeout``,
      and ``binding_refresh_interval``
    - ``clients_total`` / ``clients_connected``: number of ``Client`` instances and how many have active sockets

    Pass ``?client_id=<id>`` to include per-client detail (element count, outbox queue lengths, socket status).
    Pass ``?verbose=true`` to include a summary of all connected clients.

    The endpoint is not registered unless explicitly enabled.
    ``ui.diagnostics_view()`` calls ``collect_snapshot()`` directly and does not require the endpoint.
''')
def endpoint_demo() -> None:
    import json

    from nicegui import diagnostics

    snapshot = diagnostics.collect_snapshot()
    ui.code(json.dumps(snapshot, indent=2), language='json').classes('w-full max-h-40')


@doc.demo('Global Scope', '''
    By default the diagnostics view shows per-client detail (element count, socket status).
    Set ``scope='global'`` to show a server-wide summary (total clients, connected count) instead.
''')
def global_scope_demo() -> None:
    ui.diagnostics_view(scope='global')


@doc.demo('Auto-Refresh', '''
    Set the ``interval`` parameter to automatically refresh the diagnostics at a regular interval (in seconds).
    This is useful for monitoring memory growth or task accumulation over time.
''')
def auto_refresh_demo() -> None:
    ui.diagnostics_view(interval=5)


@doc.demo('Replace Mode', '''
    By default each refresh appends to the log history.
    Set ``mode='replace'`` to clear previous entries on each refresh,
    showing only the most recent snapshot.
''')
def replace_mode_demo() -> None:
    ui.diagnostics_view(mode='replace')


doc.reference(ui.diagnostics_view)
