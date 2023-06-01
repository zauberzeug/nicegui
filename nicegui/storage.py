import asyncio
import contextvars
import json
import threading
import uuid
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, Iterator

import aiofiles
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from . import globals

request_contextvar = contextvars.ContextVar('request_var', default=None)


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


class PersistentDict(dict):

    def __init__(self, filepath: Path, *args: Any, **kwargs: Any) -> None:
        self.filepath = filepath
        self.lock = threading.Lock()
        self.load()
        self.update(*args, **kwargs)
        self.modified = bool(args or kwargs)

    def clear(self) -> None:
        with self.lock:
            super().clear()
            self.modified = True

    def __setitem__(self, key: Any, value: Any) -> None:
        with self.lock:
            super().__setitem__(key, value)
            self.modified = True

    def __delitem__(self, key: Any) -> None:
        with self.lock:
            super().__delitem__(key)
            self.modified = True

    def load(self) -> None:
        with self.lock:
            if self.filepath.exists():
                with open(self.filepath, 'r') as f:
                    try:
                        self.update(json.load(f))
                    except json.JSONDecodeError:
                        pass

    async def backup(self) -> None:
        data = dict(self)
        if self.modified:
            async with aiofiles.open(self.filepath, 'w') as f:
                await f.write(json.dumps(data))


class RequestTrackingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_contextvar.set(request)
        if 'id' not in request.session:
            request.session['id'] = str(uuid.uuid4())
        request.state.responded = False
        response = await call_next(request)
        request.state.responded = True
        return response


class Storage:

    def __init__(self) -> None:
        self.storage_dir = Path('.nicegui')
        self.storage_dir.mkdir(exist_ok=True)
        self._general = PersistentDict(self.storage_dir / 'storage_general.json')
        self._users = PersistentDict(self.storage_dir / 'storage_users.json')

    @property
    def browser(self) -> Dict:
        """Small storage that is saved directly within the user's browser (encrypted cookie).

        The data is shared between all browser tabs and can only be modified before the initial request has been submitted.
        It is normally better to use `app.storage.user` instead to reduce payload, gain improved security and have larger storage capacity.
        """
        request: Request = request_contextvar.get()
        if request is None:
            if globals.get_client() == globals.index_client:
                raise RuntimeError('app.storage.browser can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            else:
                raise RuntimeError('app.storage.browser needs a storage_secret passed in ui.run()')
        if request.state.responded:
            return ReadOnlyDict(
                request.session,
                'the response to the browser has already been built, so modifications cannot be sent back anymore'
            )
        return request.session

    @property
    def user(self) -> Dict:
        """Individual user storage that is persisted on the server (where NiceGUI is executed).

        The data is stored in a file on the server.
        It is shared between all browser tabs by identifying the user via session cookie ID.
        """
        request: Request = request_contextvar.get()
        if request is None:
            if globals.get_client() == globals.index_client:
                raise RuntimeError('app.storage.user can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            else:
                raise RuntimeError('app.storage.user needs a storage_secret passed in ui.run()')
        if request.session['id'] not in self._users:
            self._users[request.session['id']] = {}
        return self._users[request.session['id']]

    @property
    def general(self) -> Dict:
        """General storage shared between all users that is persisted on the server (where NiceGUI is executed)."""
        return self._general

    async def backup(self) -> None:
        await self._general.backup()
        await self._users.backup()

    async def _loop(self) -> None:
        while True:
            await self.backup()
            await asyncio.sleep(1.0)
