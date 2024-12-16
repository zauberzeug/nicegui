import asyncio
import contextvars
import os
import time
import uuid
from datetime import timedelta
from pathlib import Path
from typing import Dict, Optional, Union

from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response

from . import core, observables
from .context import context
from .observables import ObservableDict
from .persistence import FilePersistentDict, PersistentDict, ReadOnlyDict, RedisPersistentDict

request_contextvar: contextvars.ContextVar[Optional[Request]] = contextvars.ContextVar('request_var', default=None)

PURGE_INTERVAL = timedelta(minutes=5).total_seconds()


class RequestTrackingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_contextvar.set(request)
        if 'id' not in request.session:
            request.session['id'] = str(uuid.uuid4())
        request.state.responded = False
        await core.app.storage._create_user_storage(request.session['id'])  # pylint: disable=protected-access
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
    """Secret key for session storage."""

    path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
    """Path to use for local persistence. Defaults to ".nicegui"."""

    redis_url = os.environ.get('NICEGUI_REDIS_URL', None)
    """URL to use for shared persistent storage via Redis. Defaults to None, which means local file storage is used."""

    redis_key_prefix = os.environ.get('NICEGUI_REDIS_KEY_PREFIX', 'nicegui:')
    """Prefix for Redis keys. Defaults to "nicegui:"."""

    max_tab_storage_age: float = timedelta(days=30).total_seconds()
    """Maximum age in seconds before tab storage is automatically purged. Defaults to 30 days."""

    def __init__(self) -> None:
        self._general = Storage._create_persistent_dict('general')
        self._users: Dict[str, PersistentDict] = {}
        self._tabs: Dict[str, PersistentDict] = {}

    @staticmethod
    def _create_persistent_dict(id: str) -> PersistentDict:  # pylint: disable=redefined-builtin
        if Storage.redis_url:
            return RedisPersistentDict(url=Storage.redis_url, id=id, key_prefix=Storage.redis_key_prefix)
        else:
            return FilePersistentDict(Storage.path / f'storage-{id}.json', encoding='utf-8')

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

        The data is stored on the server.
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
        assert session_id in self._users, f'user storage for {session_id} should be created before accessing it'
        return self._users[session_id]

    async def _create_user_storage(self, session_id: str) -> None:
        if session_id not in self._users:
            self._users[session_id] = Storage._create_persistent_dict(f'user-{session_id}')
            await self._users[session_id].initialize()

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
        assert client.tab_id in self._tabs, f'tab storage for {client.tab_id} should be created before accessing it'
        return self._tabs[client.tab_id]

    async def _create_tab_storage(self, tab_id: str) -> None:
        """Create tab storage for the given tab ID."""
        if tab_id not in self._tabs:
            self._tabs[tab_id] = Storage._create_persistent_dict(f'tab-{tab_id}')
            await self._tabs[tab_id].initialize()

    def copy_tab(self, old_tab_id: str, tab_id: str) -> None:
        """Copy the tab storage to a new tab. (For internal use only.)"""
        if old_tab_id in self._tabs:
            self._tabs[tab_id] = Storage._create_persistent_dict(f'tab-{tab_id}')
            self._tabs[tab_id].update(self._tabs[old_tab_id])

    async def prune_tab_storage(self) -> None:
        """Regularly prune tab storage that is older than the configured `max_tab_storage_age`."""
        while True:
            for tab_id, tab in list(self._tabs.items()):
                if time.time() > tab.last_modified + self.max_tab_storage_age:
                    tab.clear()
                    await tab.close()
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

    async def on_shutdown(self) -> None:
        """Close all persistent storage."""
        for user in self._users.values():
            await user.close()
        await self._general.close()
