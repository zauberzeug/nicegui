"""Server-side Yjs room manager for ui.tiptap.

Maintains one Y.Doc per doc_id and relays Yjs binary update / awareness
messages between all connected Socket.IO clients that share that doc_id.
y-py is an optional dependency; its absence is reported with a clear message.
"""
from __future__ import annotations

import asyncio
import logging
import sys
from typing import TYPE_CHECKING

from . import background_tasks, core

if TYPE_CHECKING:
    from y_py import YDoc

try:
    import y_py as Y
    HAS_Y_PY = True
    if not hasattr(Y, 'encode_state_as_update') or not hasattr(Y, 'apply_update'):
        HAS_Y_PY = False
except ImportError:
    HAS_Y_PY = False

_log = logging.getLogger(__name__)

# Process-lifetime stores — access is always from the asyncio event loop.
_docs: dict[str, YDoc] = {}        # doc_id → Y.YDoc
_rooms: dict[str, set[str]] = {}   # doc_id → set of socket-IDs


def _require_y_py() -> None:
    if not HAS_Y_PY:
        raise ImportError(
            'y-py is required for ui.tiptap state persistence. '
            'Install it with: pip install y-py'
        )


def _get_or_create_doc(doc_id: str) -> YDoc:
    _require_y_py()
    if doc_id not in _docs:
        _docs[doc_id] = Y.YDoc()
    return _docs[doc_id]


def get_state(doc_id: str) -> bytes:
    """Return the raw Yjs binary state for *doc_id* (for persistence).

    The bytes can be stored in any database (e.g. MongoDB as a ``Binary``
    field) and later restored with :func:`set_state`.  Works correctly even
    when no clients are currently connected.

    :raises ImportError: if ``y-py`` is not installed.
    """
    doc = _get_or_create_doc(doc_id)
    return bytes(Y.encode_state_as_update(doc))


def set_state(doc_id: str, data: bytes) -> None:
    """Replace the Yjs document state and broadcast it to connected clients.

    The document is replaced with a fresh Y.Doc populated from *data*, rather
    than CRDT-merged.  A plain merge cannot restore deleted content because
    CRDT deletions are permanent; a fresh document avoids this.

    Connected clients receive a ``yjs_reset`` event which causes them to
    recreate their local Y.Doc so their deletion history is also cleared.

    :param data: raw Yjs state bytes as returned by :func:`get_state`.
    :raises ImportError: if ``y-py`` is not installed.
    """
    _require_y_py()
    # Replace — not merge — so CRDT deletions in the old doc do not block restore.
    _docs[doc_id] = Y.YDoc()
    Y.apply_update(_docs[doc_id], data)
    background_tasks.create(
        _broadcast_reset(doc_id, list(data)),
        name=f'yjs_set_state_{doc_id}',
    )



async def _broadcast_reset(doc_id: str, update: list[int]) -> None:
    """Broadcast a full state reset to all clients in the room.

    Unlike ``yjs_init`` (which clients CRDT-merge), ``yjs_reset`` signals that
    clients must recreate their local Y.Doc from scratch so deletion history
    is cleared.
    """
    payload = {'doc_id': doc_id, 'update': update}
    sids = list(_rooms.get(doc_id, set()))
    await asyncio.gather(*(core.sio.emit('yjs_reset', payload, to=sid) for sid in sids))


def remove_sid(sid: str) -> None:
    """Remove a disconnected socket-ID from all rooms.

    Called by ``_on_disconnect`` in ``nicegui.py`` on every client disconnect.
    Safe to call even when y-py is not installed.
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
        if not HAS_Y_PY:
            return
        try:
            doc = _get_or_create_doc(doc_id)
            update = bytes(Y.encode_state_as_update(doc))
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
        if HAS_Y_PY:
            try:
                Y.apply_update(_get_or_create_doc(doc_id), bytes(raw))
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
    """Clean up all YDocs."""
    _docs.clear()


def reset() -> None:
    """Clear all YDocs and rooms. Called during test teardown."""
    _docs.clear()
    _rooms.clear()
