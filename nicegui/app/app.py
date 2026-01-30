import asyncio
import inspect
import os
import platform
import signal
import urllib
from collections.abc import Awaitable, Callable, Iterator
from enum import Enum
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse

from .. import background_tasks, core, helpers
from ..client import Client
from ..context import context
from ..elements.mixins.color_elements import QUASAR_COLORS
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

        self._startup_handlers: list[Callable[..., Any] | Awaitable] = []
        self._shutdown_handlers: list[Callable[..., Any] | Awaitable] = []
        self._connect_handlers: list[Callable[..., Any] | Awaitable] = []
        self._disconnect_handlers: list[Callable[..., Any] | Awaitable] = []
        self._delete_handlers: list[Callable[..., Any] | Awaitable] = []
        self._exception_handlers: list[Callable[..., Any]] = [log.exception]
        self._page_exception_handler: Callable[..., Any] | None = None

        self.colors()  # populate Quasar config with default colors

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
            self.safe_invoke(t)
        self.on_shutdown(self.storage.on_shutdown)
        self.on_shutdown(background_tasks.teardown)
        self._state = State.STARTED

    async def stop(self) -> None:
        """Stop NiceGUI. (For internal use only.)"""
        self._state = State.STOPPING
        for t in self._shutdown_handlers:
            if isinstance(t, Awaitable):
                await t
            else:
                result = t(self) if len(inspect.signature(t).parameters) == 1 else t()
                if helpers.is_coroutine_function(t):
                    await result
        self._state = State.STOPPED

    def safe_invoke(self, func: Callable[..., Any] | Awaitable) -> None:
        """Invoke the potentially async function and catch any exceptions."""
        func_name = func.__name__ if hasattr(func, '__name__') else str(func)
        try:
            if isinstance(func, Awaitable):
                async def await_func():
                    await func
                background_tasks.create(await_func(), name=f'func {func_name}')
            else:
                result = func()
                if helpers.is_coroutine_function(func) and not isinstance(result, asyncio.Task):
                    async def await_result():
                        await result
                    background_tasks.create(await_result(), name=f'result {func_name}')
        except Exception as e:
            self.handle_exception(e)

    def on_connect(self, handler: Callable | Awaitable) -> None:
        """Called every time a new client connects to NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        self._connect_handlers.append(handler)

    def on_disconnect(self, handler: Callable | Awaitable) -> None:
        """Called every time a new client disconnects from NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.

        *Updated in version 3.0.0: The handler is also called when a client reconnects.*
        """
        self._disconnect_handlers.append(handler)

    def on_delete(self, handler: Callable | Awaitable) -> None:
        """Called when a client is deleted.

        The callback has an optional parameter of `nicegui.Client`.

        *Added in version 3.0.0*
        """
        self._delete_handlers.append(handler)

    def on_startup(self, handler: Callable | Awaitable) -> None:
        """Called when NiceGUI is started or restarted.

        Needs to be called before `ui.run()`.
        """
        if self.is_started:
            if core.script_mode:
                raise RuntimeError('Unable to register a startup in script mode. Use a `@ui.page` function instead.')
            raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
        self._startup_handlers.append(handler)

    def on_shutdown(self, handler: Callable | Awaitable) -> None:
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
        if context.slot_stack and context.client is not None:
            context.client.handle_exception(exception)
        for handler in self._exception_handlers:
            result = handler() if not inspect.signature(handler).parameters else handler(exception)
            if helpers.is_coroutine_function(handler):
                background_tasks.create(result, name=f'exception {handler.__name__}')

    def on_page_exception(self, handler: Callable) -> None:
        """Called when an exception occurs in a page and allows to create a custom error page.

        The callback can accept an optional ``Exception`` as argument.
        All UI elements created in the callback are displayed on the error page.
        Asynchronous handlers are currently not supported.

        *Added in version 2.20.0*
        """
        self._page_exception_handler = handler

    def shutdown(self) -> None:
        """Shut down NiceGUI.

        This will programmatically stop the server.
        """
        if self.native.main_window:
            self.native.main_window.destroy()
        if self.config.reload or Server.instance.config.should_reload:
            os.kill(os.getppid(), getattr(signal, 'CTRL_C_EVENT' if platform.system() == 'Windows' else 'SIGINT'))
        else:
            Server.instance.should_exit = True

    def add_static_files(self,
                         url_path: str,
                         local_directory: str | Path,
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
        :param max_cache_age: value for max-age set in Cache-Control header (*added in version 2.8.0*)
        """
        if url_path == '/':
            raise ValueError('''Path cannot be "/", because it would hide NiceGUI's internal "/_nicegui" route.''')
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        handler = CacheControlledStaticFiles(
            directory=local_directory, follow_symlink=follow_symlink, max_cache_age=max_cache_age)

        @self.get(url_path.rstrip('/') + '/{path:path}')  # NOTE: prevent double slashes in route pattern
        async def static_file(request: Request, path: str = '') -> Response:
            return await handler.get_response(path, request.scope)

    def add_static_file(self, *,
                        local_file: str | Path,
                        url_path: str | None = None,
                        single_use: bool = False,
                        strict: bool = True,
                        max_cache_age: int = 3600) -> str:
        """Add a single static file.

        Allows a local file to be accessed online with enabled caching.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of files accessible, use `add_static_files()` instead.
        For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

        :param local_file: local file to serve as static content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :param single_use: whether to remove the route after the file has been downloaded once (default: False)
        :param strict: whether to raise a ``FileNotFoundError`` if the file does not exist (default: True, *added in version 2.12.0*)
        :param max_cache_age: value for max-age set in Cache-Control header (*added in version 2.8.0*)
        :return: encoded URL which can be used to access the file
        """
        if max_cache_age < 0:
            raise ValueError('''Value of max_cache_age must be a positive integer or 0.''')

        file = Path(local_file).resolve()
        if strict and not file.is_file():
            raise FileNotFoundError(f'File not found: {file}')
        path = f'/_nicegui/auto/static/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item() -> FileResponse:
            if single_use:
                self.remove_route(path)
            return FileResponse(file, headers={'Cache-Control': f'public, max-age={max_cache_age}'})

        return urllib.parse.quote(path)

    def add_media_files(self, url_path: str, local_directory: str | Path) -> None:
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
        @self.get(url_path.rstrip('/') + '/{filename:path}')  # NOTE: prevent double slashes in route pattern
        def read_item(request: Request, filename: str, nicegui_chunk_size: int = 8192) -> Response:
            local_dir = Path(local_directory).resolve()
            filepath = (local_dir / filename).resolve()
            if not filepath.is_relative_to(local_dir) or not filepath.is_file():
                raise HTTPException(status_code=404, detail='Not Found')
            return get_range_response(filepath, request, chunk_size=nicegui_chunk_size)

    def add_media_file(self, *,
                       local_file: str | Path,
                       url_path: str | None = None,
                       single_use: bool = False,
                       strict: bool = True) -> str:
        """Add a single media file.

        Allows a local file to be streamed.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of media files accessible via streaming, use `add_media_files()` instead.
        For small static files, you can use `add_static_files()` or `add_static_file()` instead.

        :param local_file: local file to serve as media content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :param single_use: whether to remove the route after the media file has been downloaded once (default: False)
        :param strict: whether to raise a ``FileNotFoundError`` if the file does not exist (default: True, *added in version 2.12.0*)
        :return: encoded URL which can be used to access the file
        """
        file = Path(local_file).resolve()
        if strict and not file.is_file():
            raise FileNotFoundError(f'File not found: {file}')
        path = f'/_nicegui/auto/media/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

        @self.get(path)
        def read_item(request: Request, nicegui_chunk_size: int = 8192) -> Response:
            if single_use:
                self.remove_route(path)
            return get_range_response(file, request, chunk_size=nicegui_chunk_size)

        return urllib.parse.quote(path)

    def colors(self, *,
               primary: str = '#5898d4',
               secondary: str = '#26a69a',
               accent: str = '#9c27b0',
               dark: str = '#1d1d1d',
               dark_page: str = '#121212',
               positive: str = '#21ba45',
               negative: str = '#c10015',
               info: str = '#31ccec',
               warning: str = '#f2c037',
               **custom_colors: str) -> None:
        """Color Theming

        Sets the main colors (primary, secondary, accent, ...) used by `Quasar <https://quasar.dev/style/theme-builder>`_ on an application-wide basis.

        Note: Use ``ui.colors()`` if you want to set colors after a page has been rendered on a per-page basis.

        *Added in version 3.6.0*

        :param primary: Primary color (default: "#5898d4")
        :param secondary: Secondary color (default: "#26a69a")
        :param accent: Accent color (default: "#9c27b0")
        :param dark: Dark color (default: "#1d1d1d")
        :param dark_page: Dark page color (default: "#121212")
        :param positive: Positive color (default: "#21ba45")
        :param negative: Negative color (default: "#c10015")
        :param info: Info color (default: "#31ccec")
        :param warning: Warning color (default: "#f2c037")
        :param custom_colors: Custom color definitions for branding
        """
        brand: dict[str, str] = self.config.quasar_config['brand']
        brand['primary'] = primary
        brand['secondary'] = secondary
        brand['accent'] = accent
        brand['dark'] = dark
        brand['dark-page'] = dark_page
        brand['positive'] = positive
        brand['negative'] = negative
        brand['info'] = info
        brand['warning'] = warning
        brand.update({name.replace('_', '-'): value for name, value in custom_colors.items()})
        QUASAR_COLORS.update({name.replace('_', '-') for name in custom_colors})

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
        self._delete_handlers.clear()
        self._exception_handlers[:] = [log.exception]
        self.config = AppConfig()
        self.colors()  # reset colors to default

    @staticmethod
    def clients(path: str) -> Iterator[Client]:
        """Iterate over all connected clients with a matching path.

        When using `@ui.page("/path")` each client gets a private view of this page.
        Updates must be sent to each client individually, which this iterator simplifies.

        *Added in version 2.7.0*

        :param path: string to filter clients by
        """
        for client in Client.instances.values():
            if client.page.path == path:
                yield client
