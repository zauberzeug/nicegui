import contextvars
import os
import uuid
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Union

import aiofiles
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response

from . import background_tasks, context, core, json, observables
from .logging import log

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

    def __init__(self, filepath: Path, encoding: Optional[str] = None) -> None:
        self.filepath = filepath
        self.encoding = encoding
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
                await f.write(json.dumps(self))
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


class Storage:

    def __init__(self) -> None:
        self.path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
        self.migrate_to_utf8()
        self._general = PersistentDict(self.path / 'storage-general.json', encoding='utf-8')
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
            if self._is_in_auto_index_context():
                raise RuntimeError('app.storage.browser can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
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
            if self._is_in_auto_index_context():
                raise RuntimeError('app.storage.user can only be used with page builder functions '
                                   '(https://nicegui.io/documentation/page)')
            raise RuntimeError('app.storage.user needs a storage_secret passed in ui.run()')
        session_id = request.session['id']
        if session_id not in self._users:
            self._users[session_id] = PersistentDict(self.path / f'storage-user-{session_id}.json', encoding='utf-8')
        return self._users[session_id]

    @staticmethod
    def _is_in_auto_index_context() -> bool:
        try:
            return context.get_client().is_auto_index_client
        except RuntimeError:
            return False  # no client

    @property
    def general(self) -> Dict:
        """General storage shared between all users that is persisted on the server (where NiceGUI is executed)."""
        return self._general

    def clear(self) -> None:
        """Clears all storage."""
        self._general.clear()
        self._users.clear()
        for filepath in self.path.glob('storage-*.json'):
            filepath.unlink()

    def migrate_to_utf8(self) -> None:
        """Migrates storage files from system's default encoding to UTF-8.

        To distinguish between the old and new encoding, the new files are named with dashes instead of underscores.
        """
        for filepath in self.path.glob('storage_*.json'):
            new_filepath = filepath.with_name(filepath.name.replace('_', '-'))
            try:
                data = json.loads(filepath.read_text())
            except Exception:
                log.warning(f'Could not load storage file {filepath}')
                data = {}
            filepath.rename(new_filepath)
            new_filepath.write_text(json.dumps(data), encoding='utf-8')
