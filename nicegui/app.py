from pathlib import Path
from typing import Awaitable, Callable, Optional, Union

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from . import globals, helpers
from .native import Native
from .storage import Storage


class App(FastAPI):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.native = Native()
        self.storage = Storage()

    def on_connect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client connects to NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        globals.connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable, Awaitable]) -> None:
        """Called every time a new client disconnects from NiceGUI.

        The callback has an optional parameter of `nicegui.Client`.
        """
        globals.disconnect_handlers.append(handler)

    def on_startup(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is started or restarted.

        Needs to be called before `ui.run()`.
        """
        if globals.state == globals.State.STARTED:
            raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
        globals.startup_handlers.append(handler)

    def on_shutdown(self, handler: Union[Callable, Awaitable]) -> None:
        """Called when NiceGUI is shut down or restarted.

        When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
        """
        globals.shutdown_handlers.append(handler)

    def on_exception(self, handler: Callable) -> None:
        """Called when an exception occurs.

        The callback has an optional parameter of `Exception`.
        """
        globals.exception_handlers.append(handler)

    def shutdown(self) -> None:
        """Shut down NiceGUI.

        This will programmatically stop the server.
        Only possible when auto-reload is disabled.
        """
        if globals.reload:
            raise Exception('calling shutdown() is not supported when auto-reload is enabled')
        globals.server.should_exit = True

    def add_static_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
        """Add a directory of static files.

        `add_static_files()` makes a local directory available at the specified endpoint, e.g. `'/static'`.
        This is useful for providing local data like images to the frontend.
        Otherwise the browser would not be able to access the files.
        Do only put non-security-critical files in there, as they are accessible to everyone.

        To make a single file accessible, you can use `add_static_file()`.
        For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

        :param url_path: string that starts with a slash "/" and identifies the path at which the files should be served
        :param local_directory: local folder with files to serve as static content
        """
        if url_path == '/':
            raise ValueError('''Path cannot be "/", because it would hide NiceGUI's internal "/_nicegui" route.''')
        globals.app.mount(url_path, StaticFiles(directory=str(local_directory)))

    def add_static_file(self, *, local_file: Union[str, Path], url_path: Optional[str] = None) -> str:
        """Add a single static file.

        Allows a local file to be accessed online with enabled caching.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of files accessible, use `add_static_files()` instead.
        For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

        :param local_file: local file to serve as static content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :return: URL path which can be used to access the file
        """
        file = Path(local_file).resolve()
        if not file.is_file():
            raise ValueError(f'File not found: {file}')
        if url_path is None:
            url_path = f'/_nicegui/auto/static/{helpers.hash_file_path(file)}/{file.name}'

        @self.get(url_path)
        async def read_item() -> FileResponse:
            return FileResponse(file, headers={'Cache-Control': 'public, max-age=3600'})

        return url_path

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
        async def read_item(request: Request, filename: str) -> StreamingResponse:
            filepath = Path(local_directory) / filename
            if not filepath.is_file():
                return {'detail': 'Not Found'}, 404
            return helpers.get_streaming_response(filepath, request)

    def add_media_file(self, *, local_file: Union[str, Path], url_path: Optional[str] = None) -> str:
        """Add a single media file.

        Allows a local file to be streamed.
        If `url_path` is not specified, a path will be generated.

        To make a whole folder of media files accessible via streaming, use `add_media_files()` instead.
        For small static files, you can use `add_static_files()` or `add_static_file()` instead.

        :param local_file: local file to serve as media content
        :param url_path: string that starts with a slash "/" and identifies the path at which the file should be served (default: None -> auto-generated URL path)
        :return: URL path which can be used to access the file
        """
        file = Path(local_file).resolve()
        if not file.is_file():
            raise ValueError(f'File not found: {local_file}')
        if url_path is None:
            url_path = f'/_nicegui/auto/media/{helpers.hash_file_path(file)}/{file.name}'

        @self.get(url_path)
        async def read_item(request: Request) -> StreamingResponse:
            return helpers.get_streaming_response(file, request)

        return url_path

    def remove_route(self, path: str) -> None:
        """Remove routes with the given path."""
        self.routes[:] = [r for r in self.routes if getattr(r, 'path', None) != path]
