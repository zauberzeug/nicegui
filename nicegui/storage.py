import asyncio
import contextvars
import os
import time
import uuid
from collections.abc import MutableMapping
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union

import aiofiles
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response

from . import background_tasks, core, json, observables
from .context import context
from .logging import log
from .observables import ObservableDict

request_contextvar: contextvars.ContextVar[Optional[Request]] = contextvars.ContextVar('request_var', default=None)

PURGE_INTERVAL = timedelta(minutes=5).total_seconds()


class ReadOnlyDict(MutableMapping):

    def __init__(self, data: Dict[Any, Any], write_error_message: str = 'Read-only dict') -> None:
        self._data: Dict[Any, Any] = data
        self._write_error_message: str = write_error_message

    def __getitem__(self, item: Any) -> Any:
        return self._data[item]

    def __setitem__(self, key: Any, value: Any) -> None:
        raise TypeError(self._write_error_message)

    def __delitem__(self, key: Any) -> None:
        raise TypeError(self._write_error_message)

    def __iter__(self) -> Iterator:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)


class PersistentDict(observables.ObservableDict):

    def __init__(self, filepath: Path, encoding: Optional[str] = None, *, indent: bool = False) -> None:
        self.filepath = filepath
        self.encoding = encoding
        self.indent = indent
        try:
            data = json.loads(filepath.read_text(encoding)) if filepath.exists() else {}
        except Exception:
            log.warning(f'Could not load storage file {filepath}')
            data = {}
        super().__init__(data, on_change=self.backup)

    def backup(self) -> None:
        """Back up the data to the given file path."""
        if not self.filepath.exists():
            if not self:
                return
            self.filepath.parent.mkdir(exist_ok=True)

        async def backup() -> None:
            async with aiofiles.open(self.filepath, 'w', encoding=self.encoding) as f:
                await f.write(json.dumps(self, indent=self.indent))
        if core.loop:
            background_tasks.create_lazy(backup(), name=self.filepath.stem)
        else:
            core.app.on_startup(backup())


class RequestTrackingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_contextvar.set(request)
        if 'id' not in request.session:
            request.session['id'] = str(uuid.uuid4())
        request.state.responded = False
        response = await call_next(request)
        request.state.responded = True
        return response


def set_storage_secret(storage_secret: Optional[str] = None) -> None:
    """Set storage_secret and add request tracking middleware."""
    if any(m.cls == SessionMiddleware for m in core.app.user_middleware):
        # NOTE not using "add_middleware" because it would be the wrong order
        core.app.user_middleware.append(Middleware(RequestTrackingMiddleware))
    elif storage_secret is not None:
        core.app.add_middleware(RequestTrackingMiddleware)
        core.app.add_middleware(SessionMiddleware, secret_key=storage_secret)
    Storage.secret = storage_secret


class Storage:
    secret: Optional[str] = None

    def __init__(self) -> None:
        self.path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
        self.max_tab_storage_age = timedelta(days=30).total_seconds()
        self._general = PersistentDict(self.path / 'storage-general.json', encoding='utf-8')
        self._users: Dict[str, PersistentDict] = {}
        self._tabs: Dict[str, observables.ObservableDict] = {}

    @property
    def browser(self) -> Union[ReadOnlyDict, Dict]:
        """Small storage that is saved directly within the user's browser (encrypted cookie).

        The data is shared between all browser tabs and can only be modified before the initial request has been submitted.
        Therefore it is normally better to use `app.storage.user` instead,
        which can be modified anytime, reduces overall payload, improves security and has larger storage capacity.
        """
        request: Optional[Request] = request_contextvar.get()
        if request is None:
            if self._is_in_auto_index_context():
                raise RuntimeError('app.storage.browser can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            if Storage.secret is None:
                raise RuntimeError('app.storage.browser needs a storage_secret passed in ui.run()')
            raise RuntimeError('app.storage.browser can only be used within a UI context')
        if request.state.responded:
            return ReadOnlyDict(
                request.session,
                'the response to the browser has already been built, so modifications cannot be sent back anymore'
            )
        return request.session

    @property
    def user(self) -> PersistentDict:
        """Individual user storage that is persisted on the server (where NiceGUI is executed).

        The data is stored in a file on the server.
        It is shared between all browser tabs by identifying the user via session cookie ID.
        """
        request: Optional[Request] = request_contextvar.get()
        if request is None:
            if self._is_in_auto_index_context():
                raise RuntimeError('app.storage.user can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            if Storage.secret is None:
                raise RuntimeError('app.storage.user needs a storage_secret passed in ui.run()')
            raise RuntimeError('app.storage.user can only be used within a UI context')
        session_id = request.session['id']
        if session_id not in self._users:
            self._users[session_id] = PersistentDict(self.path / f'storage-user-{session_id}.json', encoding='utf-8')
        return self._users[session_id]

    @staticmethod
    def _is_in_auto_index_context() -> bool:
        try:
            return context.client.is_auto_index_client
        except RuntimeError:
            return False  # no client

    @property
    def general(self) -> PersistentDict:
        """General storage shared between all users that is persisted on the server (where NiceGUI is executed)."""
        return self._general

    @property
    def client(self) -> ObservableDict:
        """A volatile storage that is only kept during the current connection to the client.

        Like `app.storage.tab` data is unique per browser tab but is even more volatile as it is already discarded
        when the connection to the client is lost through a page reload or a navigation.
        """
        if self._is_in_auto_index_context():
            raise RuntimeError('app.storage.client can only be used with page builder functions '
                               '(https://nicegui.io/documentation/page)')
        return context.client.storage

    @property
    def tab(self) -> observables.ObservableDict:
        """A volatile storage that is only kept during the current tab session."""
        if self._is_in_auto_index_context():
            raise RuntimeError('app.storage.tab can only be used with page builder functions '
                               '(https://nicegui.io/documentation/page)')
        client = context.client
        if not client.has_socket_connection:
            raise RuntimeError('app.storage.tab can only be used with a client connection; '
                               'see https://nicegui.io/documentation/page#wait_for_client_connection to await it')
        assert client.tab_id is not None
        if client.tab_id not in self._tabs:
            self._tabs[client.tab_id] = observables.ObservableDict()
        return self._tabs[client.tab_id]

    def copy_tab(self, old_tab_id: str, tab_id: str) -> None:
        """Copy the tab storage to a new tab. (For internal use only.)"""
        if old_tab_id in self._tabs:
            self._tabs[tab_id] = observables.ObservableDict(self._tabs[old_tab_id].copy())

    async def prune_tab_storage(self) -> None:
        """Regularly prune tab storage that is older than the configured `max_tab_storage_age`."""
        while True:
            for tab_id, tab in list(self._tabs.items()):
                if time.time() > tab.last_modified + self.max_tab_storage_age:
                    del self._tabs[tab_id]
            await asyncio.sleep(PURGE_INTERVAL)

    def clear(self) -> None:
        """Clears all storage."""
        self._general.clear()
        self._users.clear()
        try:
            client = context.client
        except RuntimeError:
            pass  # no client, could be a pytest
        else:
            client.storage.clear()
        self._tabs.clear()
        for filepath in self.path.glob('storage-*.json'):
            filepath.unlink()
        if self.path.exists():
            self.path.rmdir()
