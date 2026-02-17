"""Tiptap collaborative rich-text editor element backed by Tiptap + Yjs."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path

from ... import tiptap_room
from ...elements.mixins.disableable_element import DisableableElement
from ...elements.mixins.value_element import ValueElement
from ...events import GenericEventArguments, Handler, ValueChangeEventArguments

DEFAULT_TOOLBAR_BUTTONS: list[list[str]] = [
    ['bold', 'italic', 'underline', 'strike', 'code'],
    ['heading'],
    ['bullet_list', 'ordered_list'],
    ['blockquote', 'code_block'],
    ['undo', 'redo'],
]


@dataclass
class Toolbar:
    """Tiptap editor toolbar configuration.

    :param buttons: nested list of button groups, e.g. ``[['bold', 'italic'], ['undo', 'redo']]``.
        If None, uses the default button layout.

        Available button IDs: ``bold``, ``italic``, ``underline``, ``strike``, ``code``,
        ``heading`` (dropdown showing Normal/H1/H2/H3), ``h1``, ``h2``, ``h3``,
        ``bullet_list``, ``ordered_list``, ``blockquote``, ``code_block``,
        ``table``, ``undo``, ``redo``, ``hr``.

    # Future extensions: preset, position, sticky, style, compact, etc.
    """

    buttons: list[list[str]] | None = None

    def _resolve_buttons(self) -> list[list[str]]:
        """Return buttons or default if None."""
        return self.buttons if self.buttons is not None else DEFAULT_TOOLBAR_BUTTONS


class Tiptap(ValueElement, DisableableElement, component='tiptap.js',
             esm={'nicegui-tiptap': 'dist'}, default_classes='nicegui-tiptap'):
    """Collaborative rich-text editor backed by Tiptap + Yjs.

    Access the ``Toolbar`` class via ``ui.tiptap.Toolbar``.

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
    :param toolbar: toolbar configuration. Defaults to ``Toolbar()`` which shows
        the standard toolbar. Use ``None`` to hide the toolbar, or
        ``Toolbar(buttons=[...])`` for custom button groups.
        See ``Toolbar`` for available button IDs.
    :param on_change: callback invoked with a ``ValueChangeEventArguments`` whenever the HTML
        content changes.
    """

    VALUE_PROP = 'value'
    LOOPBACK = None  # Yjs (in the Vue component) owns document state; no server echo needed.

    def __init__(self, value: str = '', *, doc_id: str | None = None, user: dict[str, str] | None = None,
                 toolbar: Toolbar | None = Toolbar(),
                 on_change: Handler[ValueChangeEventArguments] | None = None) -> None:
        """Create a collaborative Tiptap rich-text editor."""
        self._doc_id = doc_id if doc_id is not None else str(uuid.uuid4())
        super().__init__(value=value, on_value_change=None)
        self.add_resource(Path(__file__).parent / 'dist')
        if on_change is not None:
            self.on_value_change(on_change)
        self._props['doc-id'] = self._doc_id
        self._props['user'] = user or {}
        self._props['toolbar'] = toolbar._resolve_buttons() if toolbar is not None else False
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

        :raises ImportError: if ``pycrdt`` is not installed (``pip install pycrdt``).
        """
        return tiptap_room.get_state(self._doc_id)

    def set_state(self, data: bytes) -> None:
        """Restore a previously persisted Yjs binary state.

        The document is replaced (not merged) so deleted content is fully
        recoverable.  All connected clients receive a reset event and recreate
        their local Yjs document from the snapshot.

        :param data: raw Yjs state bytes as returned by ``get_state()``.
        :raises ImportError: if ``pycrdt`` is not installed
            (``pip install pycrdt``).
        """
        tiptap_room.set_state(self._doc_id, data)


# Expose Toolbar as ui.tiptap.Toolbar for convenient access
Tiptap.Toolbar = Toolbar  # type: ignore[attr-defined]
