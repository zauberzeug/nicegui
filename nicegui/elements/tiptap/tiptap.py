"""Tiptap collaborative rich-text editor element backed by Tiptap + Yjs."""
from __future__ import annotations

import uuid
from pathlib import Path

from ... import tiptap_room
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments


class Tiptap(ValueElement, DisableableElement, component='tiptap.js',
             esm={'nicegui-tiptap': 'dist'}, default_classes='nicegui-tiptap'):
    """Collaborative rich-text editor backed by Tiptap + Yjs.

    Multiple browser clients sharing the same ``doc_id`` edit the same document
    in real time using CRDT conflict-free merging.  The NiceGUI Python server
    relays Yjs update and awareness messages; no external synchronisation server
    is required.

    :param value: initial HTML content (default: empty string)
    :param doc_id: collaborative room identifier; all clients using the same
        ``doc_id`` share one Yjs document.  A unique UUID is auto-generated
        when omitted, giving a per-element private document.
    :param user: cursor identity shown to collaborators,
        e.g. ``{'name': 'Alice', 'color': '#3b82f6'}``.
        Defaults to an anonymous user with a random colour.
    :param toolbar: ``True`` (default) shows the full toolbar, ``False`` hides it,
        or pass a list of lists to define custom button groups, e.g.
        ``[['bold', 'italic'], ['h1', 'h2'], ['undo', 'redo']]``.
        Available IDs: ``bold``, ``italic``, ``underline``, ``strike``, ``code``,
        ``heading`` (dropdown showing Normal/H1/H2/H3), ``h1``, ``h2``, ``h3``,
        ``bullet_list``, ``ordered_list``,
        ``blockquote``, ``code_block``, ``table``, ``undo``, ``redo``, ``hr``.
    :param on_change: callback invoked with a ``ValueChangeEventArguments`` whenever the HTML
        content changes.
    """

    VALUE_PROP = 'value'
    LOOPBACK = None  # Yjs (in the Vue component) owns document state; no server echo needed.

    def __init__(self, value: str = '', *, doc_id: str | None = None, user: dict[str, str] | None = None,
                 toolbar: bool | list[list[str]] = True,
                 on_change: Handler[ValueChangeEventArguments] | None = None) -> None:
        """Create a collaborative Tiptap rich-text editor."""
        self._doc_id = doc_id if doc_id is not None else str(uuid.uuid4())
        super().__init__(value=value, on_value_change=None)
        self.add_resource(Path(__file__).parent / 'dist')
        if on_change is not None:
            self.on_value_change(on_change)
        self._props['doc-id'] = self._doc_id
        self._props['user'] = user or {}
        self._props['toolbar'] = toolbar
        self._update_method = 'setContentFromProps'

    def _event_args_to_value(self, e: GenericEventArguments) -> str:
        """Return the HTML string emitted by Tiptap's onUpdate hook, or an empty string."""
        args = e.args
        return args if isinstance(args, str) else ''

    @property
    def doc_id(self) -> str:
        """The collaborative room identifier (read-only after construction)."""
        return self._doc_id

    def get_state(self) -> bytes:
        """Return the raw Yjs binary state of this document.

        The bytes represent a full Yjs state vector update that can be stored
        in any persistence layer (e.g. MongoDB ``Binary``, Redis, filesystem)
        and later restored with ``set_state()``.

        Works correctly even when no clients are currently connected to the room.

        :raises ImportError: if ``y-py`` is not installed (``pip install y-py``).
        """
        return tiptap_room.get_state(self._doc_id)

    def set_state(self, data: bytes) -> None:
        """Restore a previously persisted Yjs binary state.

        The document is replaced (not merged) so deleted content is fully
        recoverable.  All connected clients receive a reset event and recreate
        their local Yjs document from the snapshot.

        :param data: raw Yjs state bytes as returned by ``get_state()``.
        :raises ImportError: if ``y-py`` is not installed
            (``pip install y-py``).
        """
        tiptap_room.set_state(self._doc_id, data)
