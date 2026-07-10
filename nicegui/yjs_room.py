"""Server-side Y.Doc rooms backed by pycrdt, relayed over the Socket.IO server.

The four ``yjs_*`` events are registered as raw ``@sio.on`` handlers (not via
NiceGUI's element-level event tunnel) so that binary Yjs update payloads can stay
binary; routing them through ``this.$emit`` would JSON-stringify each Uint8Array
and inflate the wire ~5x per keystroke. Disconnect cleanup uses
``Client.on_disconnect`` instead — that's the proper NiceGUI tunnel for lifecycle.
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

# Apply binary Yjs updates above this size in a worker thread so a large paste
# doesn't stall the event loop.
_OFFLOAD_BYTES = 32 * 1024

# Engine.IO rejects incoming messages above ~1 MB (`max_http_buffer_size`), so both
# directions split larger updates into parts which the receiver reassembles in order.
_CHUNK_BYTES = 500 * 1024
_MAX_CHUNKS = 256

_rooms: dict[str, _Room] = {}
_access_checks: dict[str, list[AccessCheck]] = {}
_clients_with_hook: set[str] = set()
_handlers_installed = False


class _Room:

    def __init__(self, doc_id: str) -> None:
        assert _PycrdtDoc is not None
        self.doc_id = doc_id
        self.doc: Any = _PycrdtDoc()
        self.sids: set[str] = set()
        # pycrdt.Doc isn't thread-safe; serialize all apply_update / get_update calls.
        # The lock also serializes chunked emits so parts of two transfers never interleave.
        self.lock = asyncio.Lock()
        self.rx: dict[str, tuple[int, dict[int, bytes]]] = {}  # per-sid (parts, buffer) for chunked updates


def ensure_handlers_installed() -> None:
    """Install the Socket.IO handlers if needed. Idempotent."""
    _install_handlers_once()


def get_doc(doc_id: str) -> Any:
    """Return (creating if needed) the server-side ``pycrdt.Doc`` for ``doc_id``.

    Use this to seed initial content before any client connects. Hold
    ``_rooms[doc_id].lock`` when mutating from outside an ``@sio.on`` handler.
    """
    ensure_handlers_installed()
    return _rooms.setdefault(doc_id, _Room(doc_id)).doc


def register_access_check(doc_id: str, check: AccessCheck) -> None:
    """Register an access check (AND-combined). No checks = open room."""
    ensure_handlers_installed()
    _access_checks.setdefault(doc_id, []).append(check)


async def _check_access(doc_id: str, sid: str) -> bool:
    for check in _access_checks.get(doc_id, ()):
        result = check(doc_id, sid)
        if inspect.isawaitable(result):
            result = await result
        if not result:
            return False
    return True


def _client_id_from_sid(sid: str) -> str | None:
    try:
        environ = core.sio.get_environ(sid)
        query_bytes: bytes = environ['asgi.scope']['query_string']
        return urllib.parse.parse_qs(query_bytes.decode()).get('client_id', [None])[0]
    except (KeyError, AttributeError, UnicodeDecodeError):
        return None


def _register_client_cleanup(sid: str) -> None:
    """On first sid-join from a NiceGUI client, hook its disconnect lifecycle."""
    client_id = _client_id_from_sid(sid)
    if client_id is None or client_id in _clients_with_hook:
        return
    client = Client.instances.get(client_id)
    if client is None:
        return
    _clients_with_hook.add(client_id)
    client.on_disconnect(lambda: asyncio.create_task(_cleanup_sid(sid)))


async def _cleanup_sid(sid: str) -> None:
    for doc_id in list(_rooms):
        room = _rooms.get(doc_id)
        if room is not None and sid in room.sids:
            await _drop_client(sid, doc_id)


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
        if not await _check_access(doc_id, sid):
            return
        room = _rooms.setdefault(doc_id, _Room(doc_id))
        room.sids.add(sid)
        _register_client_cleanup(sid)
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
            if len(update_bytes) > _OFFLOAD_BYTES:
                await asyncio.to_thread(room.doc.apply_update, update_bytes)
            else:
                room.doc.apply_update(update_bytes)
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
        if isinstance(doc_id, str):
            await _drop_client(sid, doc_id)

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


async def _drop_client(sid: str, doc_id: str) -> None:
    room = _rooms.get(doc_id)
    if room is None:
        return
    room.sids.discard(sid)
    room.rx.pop(sid, None)
    await core.sio.leave_room(sid, _sio_room(doc_id))
    # Awareness removal is left to y-protocols' 30 s heartbeat — mapping sid to
    # Yjs clientID would need separate tracking and isn't worth it for an MVP.
    if not room.sids:
        _rooms.pop(doc_id, None)


def _sio_room(doc_id: str) -> str:
    return f'yjs:{doc_id}'
