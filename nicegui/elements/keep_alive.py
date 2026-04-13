from typing_extensions import Self

from ..context import context
from ..element import Element


class KeepAlive(Element, component='keep_alive_anchor.js'):

    def __init__(self) -> None:
        """Keep Alive

        Wraps its children so they stay mounted in the DOM even when the surrounding container is currently not visible
        (e.g. an inactive ``ui.tab_panel``, a closed ``ui.dialog`` or ``ui.menu``, or a sub-page that is not currently routed to).

        Method calls and events on the inner elements (such as writing to a not-yet-visible ``ui.xterm``
        or reading data from an ``ui.aggrid`` whose tab has never been opened) are dispatched as usual.

        Internally the children are rendered into a hidden host at the page root
        and teleported to the wrapper's location whenever it becomes visible.
        Note that this keeps the children alive for the full lifetime of the client, which costs memory.
        Only use it where eager mounting is actually required.

        *Added in version 3.x.0*
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
