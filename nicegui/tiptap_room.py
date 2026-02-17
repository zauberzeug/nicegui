"""Server-side Yjs room manager for ui.tiptap.

Maintains one Doc per doc_id and relays Yjs binary update / awareness
messages between all connected Socket.IO clients that share that doc_id.
pycrdt is an optional dependency; its absence is reported with a clear message.
"""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from . import background_tasks, core

if TYPE_CHECKING:
    from pycrdt import Doc

try:
    from pycrdt import Doc
    PYCRDT_AVAILABLE = True
except ImportError:
    PYCRDT_AVAILABLE = False

_log = logging.getLogger(__name__)

# Process-lifetime stores — access is always from the asyncio event loop.
_docs: dict[str, Doc] = {}        # doc_id → Doc
_rooms: dict[str, set[str]] = {}   # doc_id → set of socket-IDs


def _require_pycrdt() -> None:
    if not PYCRDT_AVAILABLE:
        raise ImportError(
            'pycrdt is required for ui.tiptap state persistence. '
            'Install it with: pip install pycrdt'
        )


def _get_or_create_doc(doc_id: str) -> Doc:
    _require_pycrdt()
    if doc_id not in _docs:
        _docs[doc_id] = Doc()
    return _docs[doc_id]


def get_state(doc_id: str) -> bytes:
    """Return the raw Yjs binary state for *doc_id* (for persistence).

    The bytes can be stored in any database (e.g. MongoDB as a ``Binary``
    field) and later restored with :func:`set_state`.  Works correctly even
    when no clients are currently connected.

    :raises ImportError: if ``pycrdt`` is not installed.
    """
    doc = _get_or_create_doc(doc_id)
    return bytes(doc.get_update())


def set_state(doc_id: str, data: bytes) -> None:
    """Replace the Yjs document state and broadcast it to connected clients.

    The document is replaced with a fresh Doc populated from *data*, rather
    than CRDT-merged.  A plain merge cannot restore deleted content because
    CRDT deletions are permanent; a fresh document avoids this.

    Connected clients receive a ``yjs_reset`` event which causes them to
    recreate their local Doc so their deletion history is also cleared.

    :param data: raw Yjs state bytes as returned by :func:`get_state`.
    :raises ImportError: if ``pycrdt`` is not installed.
    """
    _require_pycrdt()
    # Replace — not merge — so CRDT deletions in the old doc do not block restore.
    _docs[doc_id] = Doc()
    _docs[doc_id].apply_update(data)
    background_tasks.create(
        _broadcast_reset(doc_id, list(data)),
        name=f'yjs_set_state_{doc_id}',
    )



async def _broadcast_reset(doc_id: str, update: list[int]) -> None:
    """Broadcast a full state reset to all clients in the room.

    Unlike ``yjs_init`` (which clients CRDT-merge), ``yjs_reset`` signals that
    clients must recreate their local Doc from scratch so deletion history
    is cleared.
    """
    payload = {'doc_id': doc_id, 'update': update}
    sids = list(_rooms.get(doc_id, set()))
    await asyncio.gather(*(core.sio.emit('yjs_reset', payload, to=sid) for sid in sids))


def remove_sid(sid: str) -> None:
    """Remove a disconnected socket-ID from all rooms.

    Called by ``_on_disconnect`` in ``nicegui.py`` on every client disconnect.
    Safe to call even when pycrdt is not installed.
    """
    for room_sids in _rooms.values():
        room_sids.discard(sid)


def setup() -> None:
    """Register all Yjs Socket.IO event handlers on ``core.sio``.

    Called exactly once when the ``tiptap`` package is first imported.
    """

    @core.sio.on('yjs_join')
    async def _on_yjs_join(sid: str, data: dict) -> None:
        doc_id: str = data.get('doc_id', '')
        if not doc_id:
            return
        _rooms.setdefault(doc_id, set()).add(sid)
        if not PYCRDT_AVAILABLE:
            return
        try:
            doc = _get_or_create_doc(doc_id)
            update = bytes(doc.get_update())
            if len(update) > 2:  # Yjs empty-state sentinel is exactly 2 bytes
                await core.sio.emit(
                    'yjs_init',
                    {'doc_id': doc_id, 'update': list(update)},
                    to=sid,
                )
        except Exception:
            _log.exception('yjs_join: failed to send init state for doc_id=%s', doc_id)

    @core.sio.on('yjs_leave')
    def _on_yjs_leave(sid: str, data: dict) -> None:
        doc_id: str = data.get('doc_id', '')
        _rooms.get(doc_id, set()).discard(sid)

    @core.sio.on('yjs_update')
    async def _on_yjs_update(sid: str, data: dict) -> None:
        doc_id: str = data.get('doc_id', '')
        raw: list = data.get('update', [])
        if not doc_id or not raw:
            return
        if PYCRDT_AVAILABLE:
            try:
                _get_or_create_doc(doc_id).apply_update(bytes(raw))
            except Exception:
                _log.exception('yjs_update: apply failed for doc_id=%s', doc_id)
                return
        payload = {'doc_id': doc_id, 'update': raw}
        others = [s for s in _rooms.get(doc_id, set()) if s != sid]
        await asyncio.gather(*(core.sio.emit('yjs_update', payload, to=s) for s in others))

    @core.sio.on('yjs_awareness')
    async def _on_yjs_awareness(sid: str, data: dict) -> None:
        doc_id: str = data.get('doc_id', '')
        awareness: list = data.get('awareness', [])
        if not doc_id or not awareness:
            return
        payload = {'doc_id': doc_id, 'awareness': awareness}
        others = [s for s in _rooms.get(doc_id, set()) if s != sid]
        await asyncio.gather(*(core.sio.emit('yjs_awareness', payload, to=s) for s in others))



def _clear_doc(doc_id: str) -> None:
    _docs.pop(doc_id, None)


def shutdown() -> None:
    """Clean up all Docs."""
    _docs.clear()


def reset() -> None:
    """Clear all Docs and rooms. Called during test teardown."""
    _docs.clear()
    _rooms.clear()
