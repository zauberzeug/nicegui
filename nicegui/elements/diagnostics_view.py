from typing import Literal

from .. import diagnostics
from ..element import Element
from .button import Button as button
from .log import Log
from .timer import Timer as timer


class DiagnosticsView(Element):

    def __init__(self, *,
                 scope: Literal['client', 'global'] = 'client',
                 mode: Literal['append', 'replace'] = 'append',
                 interval: float | None = None,
                 ) -> None:
        """Diagnostics View

        Display a live diagnostics snapshot of the running NiceGUI application.

        :param scope: ``'client'`` shows per-client detail, ``'global'`` shows server-wide summary (default: ``'client'``)
        :param mode: ``'append'`` preserves history, ``'replace'`` clears before each refresh (default: ``'append'``)
        :param interval: auto-refresh interval in seconds; ``None`` disables auto-refresh (default: ``None``)
        """
        super().__init__()
        self._scope = scope
        self._mode = mode

        with self:
            self._log = Log().classes('w-full')
            button('Refresh', on_click=self.refresh)
            if interval is not None:
                timer(interval, self.refresh)

    def refresh(self) -> None:
        """Fetch and display a diagnostics snapshot."""
        snapshot = diagnostics.collect_snapshot(
            client_id=self.client.id if self._scope == 'client' else None,
        )

        if self._mode == 'replace':
            self._log.clear()

        server = snapshot['server']
        tasks = server['asyncio_tasks']
        memory = server['memory']

        self._log.push(f'--- {snapshot["timestamp"]} ---')
        self._log.push(f'Tasks: {tasks["total"]}')

        if self._scope == 'client' and snapshot.get('client'):
            client_info = snapshot['client']
            self._log.push(f'Elements: {client_info["elements"]}')  # pylint: disable=unsubscriptable-object
            self._log.push(f'Connected: {client_info["has_socket_connection"]}')  # pylint: disable=unsubscriptable-object
        elif self._scope == 'global':
            self._log.push(f'Clients: {server["clients_total"]} ({server["clients_connected"]} connected)')

        if memory.get('current_rss_bytes') is not None:
            mb = memory['current_rss_bytes'] / (1024 * 1024)
            self._log.push(f'Memory: {mb:.1f} MB')
