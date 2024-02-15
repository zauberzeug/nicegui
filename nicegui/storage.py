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
    """
    A read-only dictionary implementation.

    This class provides a read-only dictionary that prevents modifications to its contents.
    It is designed to be used when you want to ensure that the dictionary remains unchanged.

    Args:
        data (Dict[Any, Any]): The initial data for the dictionary.
        write_error_message (str, optional): The error message to raise when attempting to modify the dictionary.
            Defaults to 'Read-only dict'.

    Raises:
        TypeError: If any modification operation (set, delete) is attempted.
    """

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
    """
    A dictionary-like object that persists its data to a file.

    This class extends the `ObservableDict` class and adds the ability to persist
    the data to a file specified by the `filepath` parameter. The data is stored
    in JSON format.

    Parameters:
        filepath (Path): The path to the file where the data will be stored.
        encoding (Optional[str]): The encoding to use when reading and writing the file.

    Attributes:
        filepath (Path): The path to the file where the data is stored.
        encoding (Optional[str]): The encoding used when reading and writing the file.
    """

    def __init__(self, filepath: Path, encoding: Optional[str] = None) -> None:
        """
        Initialize a new instance of PersistentDict.

        Args:
            filepath (Path): The path to the file where the data will be stored.
            encoding (Optional[str]): The encoding to use when reading and writing the file.
        """
        self.filepath = filepath
        self.encoding = encoding
        try:
            data = json.loads(filepath.read_text(encoding)) if filepath.exists() else {}
        except Exception:
            log.warning(f'Could not load storage file {filepath}')
            data = {}
        super().__init__(data, on_change=self.backup)

    def backup(self) -> None:
        """
        Back up the data to the given file path.

        This method is automatically called whenever the data in the dictionary changes.
        It writes the current state of the dictionary to the file specified by `filepath`.
        If the file does not exist, it will be created. If the dictionary is empty, no
        backup will be performed.

        Note:
            This method is intended to be used internally. In most cases, you don't need
            to call it manually.

        Raises:
            OSError: If an error occurs while writing the data to the file.
        """
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
    """
    Middleware class for tracking requests and sessions.

    This middleware sets a unique identifier for each request session and tracks whether a response has been sent.
    It also provides a context variable to access the current request.

    Usage:
    1. Create an instance of RequestTrackingMiddleware and add it to your application's middleware stack.
    2. The middleware will automatically set a unique identifier for each request session.
    3. Access the current request using the request_contextvar context variable.
    4. Check the responded flag in the request state to determine if a response has been sent.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        Dispatch method called for each incoming request.

        Args:
        - request: The incoming request object.
        - call_next: The next middleware or endpoint to call.

        Returns:
        The response generated by the next middleware or endpoint.

        Raises:
        None.
        """
        request_contextvar.set(request)
        if 'id' not in request.session:
            request.session['id'] = str(uuid.uuid4())
        request.state.responded = False
        response = await call_next(request)
        request.state.responded = True
        return response


def set_storage_secret(storage_secret: Optional[str] = None) -> None:
    """
    Set the storage secret and add request tracking middleware.

    This function sets the storage secret and adds the request tracking middleware to the application's middleware stack.
    If the application already has the SessionMiddleware in its middleware stack, the request tracking middleware is appended
    to the end of the stack. Otherwise, both the request tracking middleware and the SessionMiddleware are added to the stack.

    Parameters:
        storage_secret (Optional[str]): The secret key used for encrypting session data. If None, the SessionMiddleware will not be added.

    Returns:
        None
    """
    if any(m.cls == SessionMiddleware for m in core.app.user_middleware):
        # NOTE not using "add_middleware" because it would be the wrong order
        core.app.user_middleware.append(Middleware(RequestTrackingMiddleware))
    elif storage_secret is not None:
        core.app.add_middleware(RequestTrackingMiddleware)
        core.app.add_middleware(SessionMiddleware, secret_key=storage_secret)


class Storage:
    """
    Represents a storage system for NiceGUI.

    The Storage class provides a way to store and retrieve data in NiceGUI applications.
    It consists of three types of storage:
    - browser: Small storage that is saved directly within the user's browser (encrypted cookie).
      The data is shared between all browser tabs and can only be modified before the initial request has been submitted.
      It is recommended to use `app.storage.user` instead for better flexibility and security.
    - user: Individual user storage that is persisted on the server (where NiceGUI is executed).
      The data is stored in a file on the server and is shared between all browser tabs by identifying the user via session cookie ID.
    - general: General storage shared between all users that is persisted on the server.
    """

    def __init__(self) -> None:
        self.path = Path(os.environ.get('NICEGUI_STORAGE_PATH', '.nicegui')).resolve()
        self.migrate_to_utf8()
        self._general = PersistentDict(self.path / 'storage-general.json', encoding='utf-8')
        self._users: Dict[str, PersistentDict] = {}

    @property
    def browser(self) -> Union[ReadOnlyDict, Dict]:
            """Return a small storage that is saved directly within the user's browser (encrypted cookie).

            This storage is shared between all browser tabs and can only be modified before the initial request has been submitted.
            It is recommended to use `app.storage.user` instead, which can be modified anytime, has a larger storage capacity,
            and provides better security by reducing overall payload.

            Returns:
                Union[ReadOnlyDict, Dict]: The storage object that can be used to store data.

            Raises:
                RuntimeError: If `app.storage.browser` is used outside of page builder functions or without a storage_secret passed in `ui.run()`.

            Notes:
                - The `app.storage.browser` storage is limited in capacity and should only be used for small amounts of data.
                - Modifications made to the storage after the initial request has been submitted will not be sent back to the browser.
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
            """Returns the individual user storage that is persisted on the server.

            This method retrieves the user storage for the current session. The data is stored in a file on the server,
            and it is shared between all browser tabs by identifying the user via session cookie ID.

            Returns:
                A dictionary representing the user storage.

            Raises:
                RuntimeError: If the method is called outside of a page builder function or without a storage_secret passed in ui.run().

            Example:
                To access and modify the user storage, you can use the following code:

                >>> storage = Storage()
                >>> user_storage = storage.user()
                >>> user_storage['name'] = 'John Doe'
                >>> user_storage['age'] = 30
                >>> print(user_storage['name'])
                John Doe
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
        """
        Check if the current context is in an auto index context.

        Returns:
            bool: True if the current context is in an auto index context, False otherwise.
        """
        try:
            return context.get_client().is_auto_index_client
        except RuntimeError:
            return False  # no client

    @property
    def general(self) -> Dict:
            """
            Returns the general storage shared between all users that is persisted on the server (where NiceGUI is executed).

            This method returns a dictionary object representing the general storage. The general storage is a shared storage
            that is accessible to all users of NiceGUI and is persisted on the server where NiceGUI is executed.

            Returns:
                dict: A dictionary object representing the general storage.

            Example:
                >>> storage = Storage()
                >>> general_storage = storage.general()
                >>> general_storage['key'] = 'value'
                >>> print(general_storage)
                {'key': 'value'}
            """
            return self._general

    def clear(self) -> None:
            """
            Clears all storage.

            This method clears all the data stored in the storage object. It removes all the data from the
            `_general` and `_users` dictionaries, and also deletes any storage files present in the `path`
            directory that match the pattern 'storage-*.json'.

            Usage:
                storage.clear()

            Returns:
                None
            """
            self._general.clear()
            self._users.clear()
            for filepath in self.path.glob('storage-*.json'):
                filepath.unlink()

    def migrate_to_utf8(self) -> None:
        """Migrates storage files from system's default encoding to UTF-8.

        This method is used to convert storage files from the system's default encoding to UTF-8.
        It iterates over all the storage files in the specified path that match the pattern 'storage_*.json'.
        For each file, it reads the data using the system's default encoding, and then writes the data back to the file
        using UTF-8 encoding.

        To distinguish between the old and new encoding, the new files are named with dashes instead of underscores.

        Raises:
            OSError: If there is an error while reading or writing the storage files.
            JSONDecodeError: If there is an error while decoding the JSON data.
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
