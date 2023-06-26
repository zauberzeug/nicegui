import contextvars
import json
import uuid
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union

import aiofiles
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from . import background_tasks, globals, observables

request_contextvar: contextvars.ContextVar[Optional[Request]] = contextvars.ContextVar('request_var', default=None)


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

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        data = json.loads(filepath.read_text()) if filepath.exists() else {}
        super().__init__(data, self.backup)

    def backup(self) -> None:
        async def backup() -> None:
            async with aiofiles.open(self.filepath, 'w') as f:
                await f.write(json.dumps(self))
        if globals.loop:
            background_tasks.create_lazy(backup(), name=self.filepath.stem)
        else:
            globals.app.on_startup(backup())


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
        self._users: Dict[str, PersistentDict] = {}

    @property
    def browser(self) -> Union[ReadOnlyDict, Dict]:
        """Small storage that is saved directly within the user's browser (encrypted cookie).

        The data is shared between all browser tabs and can only be modified before the initial request has been submitted.
        Therefore it is normally better to use `app.storage.user` instead,
        which can be modified anytime, reduces overall payload, improves security and has larger storage capacity.
        """
        request: Optional[Request] = request_contextvar.get()
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
        request: Optional[Request] = request_contextvar.get()
        if request is None:
            if globals.get_client() == globals.index_client:
                raise RuntimeError('app.storage.user can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            else:
                raise RuntimeError('app.storage.user needs a storage_secret passed in ui.run()')
        id = request.session['id']
        if id not in self._users:
            self._users[id] = PersistentDict(self.storage_dir / f'storage_user_{id}.json')
        return self._users[id]

    @property
    def general(self) -> Dict:
        """General storage shared between all users that is persisted on the server (where NiceGUI is executed)."""
        return self._general

    def clear(self) -> None:
        """Clears all storage."""
        self._general.clear()
        self._users.clear()
        for filepath in self.storage_dir.glob('storage_*.json'):
            filepath.unlink()
