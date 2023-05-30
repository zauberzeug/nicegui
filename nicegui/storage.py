import asyncio
import contextvars
import json
import threading
import uuid
from pathlib import Path
from typing import Dict

import aiofiles
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

request_contextvar = contextvars.ContextVar('request_var', default=None)


class ReadOnlyDict:
    def __init__(self, data: Dict, write_error_message: str = 'Read-only dict'):
        self._data = data
        self._write_error_message = write_error_message

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        raise TypeError(self._write_error_message)


class PersistentDict(dict):
    def __init__(self, filename: Path, *arg, **kw):
        self.filename = filename
        self.lock = threading.Lock()
        self.load()
        self.update(*arg, **kw)
        self.modified = bool(arg or kw)

    def load(self):
        with self.lock:
            if self.filename.exists():
                with open(self.filename, 'r') as f:
                    try:
                        self.update(json.load(f))
                    except json.JSONDecodeError:
                        pass

    def __setitem__(self, key, value):
        with self.lock:
            super().__setitem__(key, value)
            self.modified = True

    def __delitem__(self, key):
        with self.lock:
            super().__delitem__(key)
            self.modified = True

    def clear(self):
        with self.lock:
            super().clear()
            self.modified = True

    async def backup(self):
        data = dict(self)
        if self.modified:
            async with aiofiles.open(self.filename, 'w') as f:
                await f.write(json.dumps(data))


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_contextvar.set(request)
        if 'id' not in request.session:
            request.session['id'] = str(uuid.uuid4())
        request.state.responded = False
        response = await call_next(request)
        request.state.responded = True
        return response


class Storage:

    def __init__(self):
        self.storage_dir = Path('.nicegui')
        self.storage_dir.mkdir(exist_ok=True)
        self._general = PersistentDict(self.storage_dir / 'storage_general.json')
        self._individuals = PersistentDict(self.storage_dir / 'storage_individuals.json')

    @property
    def browser(self) -> Dict:
        """Small storage that is saved directly within the user's browser (encrypted cookie).

        The data is shared between all browser tab and can only be modified before the initial request has been submitted.
        Normally it is better to use `app.storage.individual` instead to reduce payload, improved security and larger storage capacity)."""
        request: Request = request_contextvar.get()
        if request is None:
            raise RuntimeError('storage.browser needs a storage_secret passed in ui.run()')
        if request.state.responded:
            return ReadOnlyDict(
                request.session,
                'the response to the browser has already been build so modifications can not be send back anymore'
            )
        return request.session

    @property
    def individual(self) -> Dict:
        """Individual user storage that is persisted on the server (where NiceGUI is executed).

        The data is stored in a file on the server.
        It is shared between all browser tabs by identifying the user via session cookie id.
        """
        request: Request = request_contextvar.get()
        if request is None:
            raise RuntimeError('storage.individual needs a storage_secret passed in ui.run()')
        if request.session['id'] not in self._individuals:
            self._individuals[request.session['id']] = {}
        return self._individuals[request.session['id']]

    @property
    def general(self) -> Dict:
        """General storage shared between all users that is persisted on the server (where NiceGUI is executed)."""
        return self._general

    async def backup(self):
        await self._general.backup()
        await self._individuals.backup()

    async def _loop(self):
        while True:
            await self.backup()
            await asyncio.sleep(10)
