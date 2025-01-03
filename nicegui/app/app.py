import inspect
import os
import platform
import signal
import urllib
from enum import Enum
from pathlib import Path
from typing import Any, Awaitable, Callable, Iterator, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse

from .. import background_tasks, helpers
from ..client import Client
from ..logging import log
from ..native import NativeConfig
from ..observables import ObservableSet
from ..server import Server
from ..staticfiles import CacheControlledStaticFiles
from ..storage import Storage
from .app_config import AppConfig
from .range_response import get_range_response


class State(Enum):
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


class App(FastAPI):
    from ..timer import Timer as timer  # pylint: disable=import-outside-toplevel

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, docs_url=None, redoc_url=None, openapi_url=None)
        self.native = NativeConfig()
        self.storage = Storage()
        self.urls = ObservableSet()
        self._state: State = State.STOPPED
        self.config = AppConfig()

        self._startup_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._shutdown_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._connect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._disconnect_handlers: List[Union[Callable[..., Any], Awaitable]] = []
        self._exception_handlers: List[Callable[..., Any]] = [log.exception]

    @property
    def is_starting(self) -> bool:
        """Return whether NiceGUI is starting."""
        return self._state == State.STARTING

    @property
    def is_started(self) -> bool:
        """Return whether NiceGUI is started."""
        return self._state == State.STARTED

    @property
    def is_stopping(self) -> bool:
        """Return whether NiceGUI is stopping."""
        return self._state == State.STOPPING

    @property
    def is_stopped(self) -> bool:
        """Return whether NiceGUI is stopped."""
        return self._state == State.STOPPED

    def start(self) -> None:
        """Start NiceGUI. (For internal use only.)"""
        self._state = State.STARTING
        for t in self._startup_handlers:
            Client.auto_index_client.safe_invoke(t)
        self._state = State.STARTED

    def stop(self) -> None:
        """Stop NiceGUI. (For internal use only.)"""
        self._state = State.STOPPING
        for t in self._shutdown_handlers:
            Client.auto_index_client.safe_invoke(t)
        self._state = State.STOPPED

    def on_connect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client connects to NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        self._connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client disconnects from NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        self._disconnect_handlers.append(handler)

    def on_startup(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is started or restarted.

        Needs to be called before `ui.run()`.
        """
        if self.is_started:
            raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
        self._startup_handlers.append(handler)

    def on_shutdown(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is shut down or restarted.

        When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
        """
        self._shutdown_handlers.append(handler)

    def on_exception(self, handler: Callable) -> None:
        """Called when an exception occurs.

        The callback has an optional parameter of `Exception`.
        """
        self._exception_handlers.append(handler)

    def handle_exception(self, exception: Exception) -> None:
        """Handle an exception by invoking all registered exception handlers."""
        for handler in self._exception_handlers:
            result = handler() if not inspect.signature(handler).parameters else handler(exception)
            if helpers.is_coroutine_function(handler):
                background_tasks.create(result)

    def shutdown(self) -> None:
        """Shut down NiceGUI.

        This will programmatically stop the server.
        """
        if self.native.main_window:
            self.native.main_window.destroy()
        if self.config.reload:
            os.kill(os.getppid(), getattr(signal, 'CTRL_C_EVENT' if platform.system() == 'Windows' else 'SIGINT'))
        else:
            Server.instance.should_exit = True

    def add_static_files(self,
                         url_path: str,
                         local_directory: Union[str, Path],
                         *,
                         follow_symlink: bool = False,
                         max_cache_age: int = 3600) -> None:
        """Add a directory of static files.

        `add_static_files()` makes a local directory available at the specified endpoint, e.g. `'/static'`.
        This is useful for providing local data like images to the frontend.
        Otherwise the browser would not be able to access the files.
        Do only put non-security-critical files in there, as they are accessible to everyone.

        To make a single file accessible, you can use `add_static_file()`.
        For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

        :param url_path: string that starts with a slash "/" and identifies the path at which the files should be served
        :param local_directory: local folder with files to serve as static content
        :param follow_symlink: whether to follow symlinks (default: False)
        :param max_cache_age: value for max-age set in Cache-Control header
        """
        if url_path == '/':
            raise ValueError('''Path cannot be "/", because it would hide NiceGUI's internal "/_nicegui" route.''')
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        handler = CacheControlledStaticFiles(
            directory=local_directory, follow_symlink=follow_symlink, max_cache_age=max_cache_age)

        @self.get(url_path + '/{path:path}')
        async def static_file(request: Request, path: str = '') -> Response:
            return await handler.get_response(path, request.scope)

    def add_static_file(self, *,
                        local_file: Union[str, Path],
                        url_path: Optional[str] = None,
                        single_use: bool = False,
                        max_cache_age: int = 3600) -> str:
        """Add a single static file.

        Allows a local file to be accessed online with enabled caching.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of files accessible, use `add_static_files()` instead.
        For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

        :param local_file: local file to serve as static content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :param single_use: whether to remove the route after the file has been downloaded once (default: False)
        :param max_cache_age: value for max-age set in Cache-Control header
        :return: encoded URL which can be used to access the file
        """
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        file = Path(local_file).resolve()
        if not file.is_file():
            raise ValueError(f'File not found: {file}')
        path = f'/_nicegui/auto/static/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item() -> FileResponse:
            if single_use:
                self.remove_route(path)
            return FileResponse(file, headers={'Cache-Control': f'public, max-age={max_cache_age}'})

        return urllib.parse.quote(path)

    def add_media_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        """Add directory of media files.

        `add_media_files()` allows a local files to be streamed from a specified endpoint, e.g. `'/media'`.
        This should be used for media files to support proper streaming.
        Otherwise the browser would not be able to access and load the the files incrementally or jump to different positions in the stream.
        Do only put non-security-critical files in there, as they are accessible to everyone.

        To make a single file accessible via streaming, you can use `add_media_file()`.
        For small static files, you can use `add_static_files()` or `add_static_file()` instead.

        :param url_path: string that starts with a slash "/" and identifies the path at which the files should be served
        :param local_directory: local folder with files to serve as media content
        """
        @self.get(url_path + '/{filename:path}')
        def read_item(request: Request, filename: str, nicegui_chunk_size: int = 8192) -> Response:
            filepath = Path(local_directory) / filename
            if not filepath.is_file():
                raise HTTPException(status_code=404, detail='Not Found')
            return get_range_response(filepath, request, chunk_size=nicegui_chunk_size)

    def add_media_file(self, *,
                       local_file: Union[str, Path],
                       url_path: Optional[str] = None,
                       single_use: bool = False,
                       ) -> str:
        """Add a single media file.

        Allows a local file to be streamed.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of media files accessible via streaming, use `add_media_files()` instead.
        For small static files, you can use `add_static_files()` or `add_static_file()` instead.

        :param local_file: local file to serve as media content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :param single_use: whether to remove the route after the media file has been downloaded once (default: False)
        :return: encoded URL which can be used to access the file
        """
        file = Path(local_file).resolve()
        if not file.is_file():
            raise ValueError(f'File not found: {local_file}')
        path = f'/_nicegui/auto/media/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item(request: Request, nicegui_chunk_size: int = 8192) -> Response:
            if single_use:
                self.remove_route(path)
            return get_range_response(file, request, chunk_size=nicegui_chunk_size)

        return urllib.parse.quote(path)

    def remove_route(self, path: str) -> None:
        """Remove routes with the given path."""
        self.routes[:] = [r for r in self.routes if getattr(r, 'path', None) != path]

    def reset(self) -> None:
        """Reset app to its initial state. (Useful for testing.)"""
        self.storage.clear()
        self._startup_handlers.clear()
        self._shutdown_handlers.clear()
        self._connect_handlers.clear()
        self._disconnect_handlers.clear()
        self._exception_handlers[:] = [log.exception]

    @staticmethod
    def clients(path: str) -> Iterator[Client]:
        """Iterate over all connected clients with a matching path.

        When using `@ui.page("/path")` each client gets a private view of this page.
        Updates must be sent to each client individually, which this iterator simplifies.

        :param path: string to filter clients by
        """
        for client in Client.instances.values():
            if client.page.path == path:
                yield client
