"""Server-side Y.Doc rooms backed by pycrdt, relayed over the Socket.IO server.

The four ``yjs_*`` events are registered as raw ``@sio.on`` handlers (not via
NiceGUI's element-level event tunnel) so that binary Yjs update payloads can stay
binary; routing them through ``this.$emit`` would JSON-stringify each Uint8Array
and inflate the wire ~5x per keystroke.

Lifecycle follows NiceGUI's client model, not Socket.IO's: sids are ephemeral
(every transient reconnect mints a new one), so live sids are tracked only for
relaying, while room membership and eviction are keyed to the ``Client`` —
sids drop on ``on_disconnect``, rooms evict once their last client is deleted.
"""
from __future__ import annotations

import asyncio
import inspect
import urllib.parse
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from . import core, optional_features
from .client import Client
from .dependencies import register_esm
from .logging import log

try:
    from pycrdt import Doc as _PycrdtDoc
    optional_features.register('pycrdt')
except ImportError:
    _PycrdtDoc = None  # type: ignore[assignment, misc]

# Shared yjs core bundle, registered like any other element-level ESM module.
# Consumers (ui.codemirror today, ui.tiptap tomorrow) mark `yjs` external in their
# own rollup and inline whatever protocol helpers they need (y-protocols/awareness,
# y-prosemirror, etc.) — those are tiny and consumer-specific.
_YJS_DIST = Path(__file__).parent / 'elements' / '_yjs_bundle' / 'dist'
if _YJS_DIST.is_dir():
    register_esm('yjs', _YJS_DIST, max_time=_YJS_DIST.stat().st_mtime)

AccessCheck = Callable[[str, str], bool | Awaitable[bool]]

# Engine.IO rejects incoming messages above ~1 MB (`max_http_buffer_size`), so both
# directions split larger updates into parts which the receiver reassembles in order.
_CHUNK_BYTES = 500 * 1024
_MAX_CHUNKS = 256

_rooms: dict[str, _Room] = {}
_access_checks: dict[str, AccessCheck] = {}
_client_sids: dict[str, set[str]] = {}
_clients_with_hook: set[str] = set()
_handlers_installed = False


class _Room:

    def __init__(self, doc_id: str) -> None:
        assert _PycrdtDoc is not None
        self.doc_id = doc_id
        self.doc: Any = _PycrdtDoc()
        self.sids: set[str] = set()  # live sockets to relay to (ephemeral across reconnects)
        self.clients: set[str] = set()  # client ids keeping the room alive
        # pycrdt.Doc isn't thread-safe; serialize all apply_update / get_update calls.
        # The lock also serializes chunked emits so parts of two transfers never interleave.
        self.lock = asyncio.Lock()
        self.rx: dict[str, tuple[int, dict[int, bytes]]] = {}  # per-sid (parts, buffer) for chunked updates


def ensure_handlers_installed() -> None:
    """Install the Socket.IO handlers if needed. Idempotent."""
    _install_handlers_once()


def get_doc(doc_id: str) -> Any:
    """Return (creating if needed) the server-side ``pycrdt.Doc`` for ``doc_id``.

    Use this to seed initial content before any client connects;
    once clients are connected, mutations must happen on the event loop
    (e.g. in an event handler), never from a worker thread.
    """
    ensure_handlers_installed()
    return _rooms.setdefault(doc_id, _Room(doc_id)).doc


def register_access_check(doc_id: str, check: AccessCheck) -> None:
    """Register the access check for a room, replacing any previous one. No check = open room."""
    ensure_handlers_installed()
    _access_checks[doc_id] = check


async def _check_access(doc_id: str, sid: str) -> bool:
    check = _access_checks.get(doc_id)
    if check is None:
        return True
    result = check(doc_id, sid)
    if inspect.isawaitable(result):
        result = await result
    return bool(result)


def _client_id_from_sid(sid: str) -> str | None:
    try:
        environ = core.sio.get_environ(sid)
        query_bytes: bytes = environ['asgi.scope']['query_string']
        return urllib.parse.parse_qs(query_bytes.decode()).get('client_id', [None])[0]
    except (KeyError, AttributeError, UnicodeDecodeError):
        return None


def _hook_client_lifecycle(client: Client, client_id: str) -> None:
    """Track room membership per client: sids drop on disconnect, rooms evict on delete.

    ``on_disconnect`` also fires on transient reconnects (new sid incoming),
    so it must never evict; the browser re-joins with its new sid right after.
    """
    async def handle_disconnect() -> None:
        # This handler runs as a background task, possibly AFTER the browser has already
        # re-joined with a new sid — so only drop sids whose socket is actually gone.
        sids = _client_sids.get(client_id, set())
        for sid in [s for s in sids if not core.sio.manager.is_connected(s, '/')]:
            sids.discard(sid)
            await _drop_sid(sid)

    async def handle_delete() -> None:
        _clients_with_hook.discard(client_id)
        for sid in _client_sids.pop(client_id, set()):
            await _drop_sid(sid)
        for doc_id, room in list(_rooms.items()):
            if client_id in room.clients:
                room.clients.discard(client_id)
                _evict_if_abandoned(doc_id)

    client.on_disconnect(handle_disconnect)
    client.on_delete(handle_delete)


async def _drop_sid(sid: str) -> None:
    for doc_id, room in list(_rooms.items()):
        if sid in room.sids:
            room.sids.discard(sid)
            room.rx.pop(sid, None)
            await core.sio.leave_room(sid, _sio_room(doc_id))


def _evict_if_abandoned(doc_id: str) -> None:
    room = _rooms.get(doc_id)
    # Awareness removal is left to y-protocols' 30 s heartbeat — mapping sid to
    # Yjs clientID would need separate tracking and isn't worth it for an MVP.
    if room is not None and not room.clients:
        _rooms.pop(doc_id, None)


def _install_handlers_once() -> None:
    global _handlers_installed  # pylint: disable=global-statement # noqa: PLW0603
    if _handlers_installed:
        return
    if _PycrdtDoc is None:
        raise RuntimeError('pycrdt is not installed; `pip install "nicegui[crdt]"`')
    sio = core.sio

    @sio.on('yjs_join')
    async def _on_join(sid: str, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            return
        doc_id = data.get('doc_id')
        if not isinstance(doc_id, str):
            return
        client_id = _client_id_from_sid(sid)
        client = Client.instances.get(client_id) if client_id is not None else None
        if client_id is None or client is None:
            return  # only sockets belonging to a live NiceGUI client may join (and get cleaned up)
        if not await _check_access(doc_id, sid):
            return
        room = _rooms.setdefault(doc_id, _Room(doc_id))
        room.sids.add(sid)
        room.clients.add(client_id)
        _client_sids.setdefault(client_id, set()).add(sid)
        if client_id not in _clients_with_hook:
            _clients_with_hook.add(client_id)
            _hook_client_lifecycle(client, client_id)
        await sio.enter_room(sid, _sio_room(doc_id))
        async with room.lock:
            state: bytes = room.doc.get_update()
            await _emit_chunked('yjs_init', doc_id, state, to=sid)

    @sio.on('yjs_update')
    async def _on_update(sid: str, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            return
        doc_id = data.get('doc_id')
        update = data.get('update')
        if not isinstance(doc_id, str) or not isinstance(update, (bytes, bytearray)):
            return
        room = _rooms.get(doc_id)
        if room is None or sid not in room.sids:
            return
        update_bytes = _reassemble(room, sid, bytes(update), data)
        if update_bytes is None:
            return
        async with room.lock:
            try:
                room.doc.apply_update(update_bytes)
            except ValueError:
                log.warning('dropping malformed Yjs update for room "%s"', doc_id)
                return
            await _emit_chunked('yjs_update', doc_id, update_bytes, room=_sio_room(doc_id), skip_sid=sid)

    @sio.on('yjs_awareness')
    async def _on_awareness(sid: str, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            return
        doc_id = data.get('doc_id')
        update = data.get('update')
        if not isinstance(doc_id, str) or not isinstance(update, (bytes, bytearray)):
            return
        room = _rooms.get(doc_id)
        if room is None or sid not in room.sids:
            return
        await sio.emit('yjs_awareness', {'doc_id': doc_id, 'update': bytes(update)},
                       room=_sio_room(doc_id), skip_sid=sid)

    @sio.on('yjs_leave')
    async def _on_leave(sid: str, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            return
        doc_id = data.get('doc_id')
        if not isinstance(doc_id, str):
            return
        room = _rooms.get(doc_id)
        if room is None:
            return
        room.sids.discard(sid)
        room.rx.pop(sid, None)
        await sio.leave_room(sid, _sio_room(doc_id))
        client_id = _client_id_from_sid(sid)
        if client_id is not None:
            room.clients.discard(client_id)
            # NOTE: the sid stays in _client_sids — it may still be a member of other rooms.
        _evict_if_abandoned(doc_id)

    _handlers_installed = True


async def _emit_chunked(event: str, doc_id: str, update: bytes, **emit_kwargs: Any) -> None:
    if len(update) <= _CHUNK_BYTES:
        await core.sio.emit(event, {'doc_id': doc_id, 'update': update}, **emit_kwargs)
        return
    parts = [update[i:i + _CHUNK_BYTES] for i in range(0, len(update), _CHUNK_BYTES)]
    for i, part in enumerate(parts):
        await core.sio.emit(event, {'doc_id': doc_id, 'update': part, 'part': i, 'parts': len(parts)},
                            **emit_kwargs)


def _reassemble(room: _Room, sid: str, update: bytes, data: dict[str, Any]) -> bytes | None:
    """Buffer chunked updates until complete; return the full update or ``None`` while pending.

    Parts are keyed by index rather than appended, so reassembly does not depend on
    Socket.IO's ``async_handlers`` background tasks preserving dispatch order.
    """
    parts = data.get('parts')
    if parts is None:
        return update
    part = data.get('part')
    if not isinstance(parts, int) or not isinstance(part, int) or not 2 <= parts <= _MAX_CHUNKS or not 0 <= part < parts:
        room.rx.pop(sid, None)
        return None
    if sid not in room.rx or room.rx[sid][0] != parts:  # new transfer supersedes any stale one
        room.rx[sid] = (parts, {})
    buffer = room.rx[sid][1]
    buffer[part] = update
    if len(buffer) < parts:
        return None
    room.rx.pop(sid, None)
    return b''.join(buffer[i] for i in range(parts))


def _sio_room(doc_id: str) -> str:
    return f'yjs:{doc_id}'
