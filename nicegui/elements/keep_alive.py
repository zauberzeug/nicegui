from typing_extensions import Self

from ..context import context
from ..element import Element


class KeepAlive(Element, component='keep_alive_anchor.js'):

    def __init__(self) -> None:
        """Keep Alive

        Wraps its children so they stay mounted in the DOM even when the surrounding container is currently not visible
        (e.g. an inactive ``ui.tab_panel``, a closed ``ui.dialog`` or ``ui.menu``, or a sub-page that is not currently routed to).

        This is useful for elements whose client-side state would otherwise be lost or unreachable before first display:
        writing to a ``ui.xterm`` inside a never-opened tab, reading ``ui.aggrid.get_client_data()`` from a closed dialog,
        or preserving edit history in a ``ui.codemirror`` across navigation.
        Method calls and events on the inner elements are executed immediately on the live component instance —
        they are never buffered or replayed.

        Internally the children are rendered into a hidden host at the page root
        and teleported to the wrapper's location whenever it becomes visible.
        As a consequence, the server-side element tree parents the children to this host, not to the surrounding container:
        ``descendants()`` on the apparent parent and scoped ``ui.element_filter`` will not traverse into the subtree.
        Keep a direct reference to the inner elements if you need to reach them programmatically.

        Note that this keeps the children alive for the full lifetime of the client, which costs memory.
        Only use it where eager mounting is actually required.

        *Added in version 3.11.0*
        """
        super().__init__()
        with context.client.layout:
            self._host = _KeepAliveHost(anchor=self)
        self._props['host-id'] = self._host.id

    def __enter__(self) -> Self:
        # Children declared inside `with ui.keep_alive(): ...` belong to the stable host,
        # not to the anchor that may be unmounted at any time.
        self._host.__enter__()
        return self

    def __exit__(self, *exc) -> None:
        self._host.__exit__(*exc)

    def _handle_delete(self) -> None:
        # NOTE: the host may already be queued for deletion if the entire client is being torn down,
        # in which case its parent slot has already cleared it from its children list.
        host_slot = self._host.parent_slot
        if not self._host.is_deleted and host_slot is not None and self._host in host_slot.children:
            self._host.delete()
        super()._handle_delete()


class _KeepAliveHost(Element, component='keep_alive_host.js'):

    def __init__(self, *, anchor: Element) -> None:
        super().__init__()
        self._props['anchor-selector'] = f'#{anchor.html_id}'
