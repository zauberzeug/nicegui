import inspect
from enum import Enum
from pathlib import Path
from typing import Any, Awaitable, Callable, List, Optional, Union

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .. import background_tasks, helpers
from ..client import Client
from ..logging import log
from ..native import NativeConfig
from ..observables import ObservableSet
from ..server import Server
from ..storage import Storage
from .app_config import AppConfig
from .range_response import get_range_response


class State(Enum):
    """
    Enum representing the possible states of an application.

    The State enum provides a set of predefined states that an application can be in.
    Each state is represented by a unique value.

    Attributes:
        - STOPPED (int): Represents the stopped state of the application. Value: 0.
        - STARTING (int): Represents the starting state of the application. Value: 1.
        - STARTED (int): Represents the started state of the application. Value: 2.
        - STOPPING (int): Represents the stopping state of the application. Value: 3.

    Example:
        >>> current_state = State.STARTED
        >>> print(current_state)
        State.STARTED
        >>> print(current_state.value)
        2
    """
    STOPPED = 0
    STARTING = 1
    STARTED = 2
    STOPPING = 3


class App(FastAPI):
    """
    The main application class for NiceGUI.

    This class extends the FastAPI framework and provides additional functionality for building NiceGUI applications.

    Attributes:
        - native (NativeConfig): The native configuration object.
        - storage (Storage): The storage object for managing data persistence.
        - urls (ObservableSet): The set of URLs registered in the application.
        - _state (State): The current state of the application.
        - config (AppConfig): The configuration object for the application.

    Methods:
        is_starting() -> bool: Returns whether NiceGUI is starting.
        is_started() -> bool: Returns whether NiceGUI is started.
        is_stopping() -> bool: Returns whether NiceGUI is stopping.
        is_stopped() -> bool: Returns whether NiceGUI is stopped.
        start() -> None: Starts NiceGUI. (For internal use only.)
        stop() -> None: Stops NiceGUI. (For internal use only.)
        on_connect(handler: Union[Callable, Awaitable]) -> None: Registers a handler to be called when a new client connects to NiceGUI.
        on_disconnect(handler: Union[Callable, Awaitable]) -> None: Registers a handler to be called when a client disconnects from NiceGUI.
        on_startup(handler: Union[Callable, Awaitable]) -> None: Registers a handler to be called when NiceGUI is started or restarted.
        on_shutdown(handler: Union[Callable, Awaitable]) -> None: Registers a handler to be called when NiceGUI is shut down or restarted.
        on_exception(handler: Callable) -> None: Registers a handler to be called when an exception occurs.
        handle_exception(exception: Exception) -> None: Handles an exception by invoking all registered exception handlers.
        shutdown() -> None: Shuts down NiceGUI programmatically.
        add_static_files(url_path: str, local_directory: Union[str, Path], follow_symlink: bool = False) -> None: Adds a directory of static files.
        add_static_file(local_file: Union[str, Path], url_path: Optional[str] = None, single_use: bool = False) -> str: Adds a single static file.
        add_media_files(url_path: str, local_directory: Union[str, Path]) -> None: Adds a directory of media files.
        add_media_file(local_file: Union[str, Path], url_path: Optional[str] = None, single_use: bool = False) -> str: Adds a single media file.
    """
    def __init__(self, **kwargs) -> None:
            """
            App class

            Args:
               - **kwargs: Additional keyword arguments.

            Attributes:
                - native (NativeConfig): An instance of the NativeConfig class.
                - storage (Storage): An instance of the Storage class.
                - urls (ObservableSet): A set of URLs.
                - _state (State): The current state of the app.
                - config (AppConfig): An instance of the AppConfig class.
                - _startup_handlers (List[Union[Callable[..., Any], Awaitable]]): A list of startup handlers.
                - _shutdown_handlers (List[Union[Callable[..., Any], Awaitable]]): A list of shutdown handlers.
                - _connect_handlers (List[Union[Callable[..., Any], Awaitable]]): A list of connect handlers.
                - _disconnect_handlers (List[Union[Callable[..., Any], Awaitable]]): A list of disconnect handlers.
                - _exception_handlers (List[Callable[..., Any]]): A list of exception handlers.

            """
            super().__init__(**kwargs)
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
        """
        Return whether NiceGUI is starting.

        This method checks the current state of NiceGUI and returns True if it is in the starting state,
        and False otherwise.

        Return:
            - True if NiceGUI is starting, False otherwise.
            :type: bool
        """
        return self._state == State.STARTING

    @property
    def is_started(self) -> bool:
            """
            Return whether NiceGUI is started.

            This method checks the current state of NiceGUI and returns True if it is in the STARTED state,
            indicating that NiceGUI has been started. Otherwise, it returns False.

            Returns:
                bool: True if NiceGUI is started, False otherwise.

            Example:
                >>> app = NiceGUIApp()
                >>> app.start()
                >>> app.is_started()
                True
            """
            return self._state == State.STARTED

    @property
    def is_stopping(self) -> bool:
            """
            Return whether NiceGUI is stopping.

            This method checks the current state of NiceGUI and returns True if NiceGUI is in the stopping state,
            and False otherwise.

            Returns:
                bool: True if NiceGUI is stopping, False otherwise.

            Example:
                >>> app = NiceGUIApp()
                >>> app.is_stopping()
                False

            Note:
                NiceGUI can be in different states, such as STARTING, RUNNING, or STOPPING. This method specifically
                checks for the STOPPING state.

            See Also:
                - NiceGUIApp.start: Method to start NiceGUI.
                - NiceGUIApp.stop: Method to stop NiceGUI.
                - NiceGUIApp.get_state: Method to get the current state of NiceGUI.
            """
            return self._state == State.STOPPING

    @property
    def is_stopped(self) -> bool:
        """
        Return whether NiceGUI is stopped.

        This method checks the current state of NiceGUI and returns True if it is in the stopped state,
        and False otherwise.

        :return: A boolean value indicating whether NiceGUI is stopped.
        :rtype: bool
        """
        return self._state == State.STOPPED

    def start(self) -> None:
            """Start NiceGUI.

            This method is used to start the NiceGUI application. It sets the internal state to 'STARTING',
            invokes the startup handlers, and then sets the state to 'STARTED'.

            Usage:
                Call this method to start the NiceGUI application.

            Returns:
                None

            Raises:
                None
            """
            self._state = State.STARTING
            for t in self._startup_handlers:
                Client.auto_index_client.safe_invoke(t)
            self._state = State.STARTED

    def stop(self) -> None:
            """
            Stop NiceGUI. (For internal use only.)

            This method is used to stop the NiceGUI application. It changes the state of the application to 'STOPPING',
            invokes the shutdown handlers, and then sets the state to 'STOPPED'.

            Note:
                This method is intended for internal use only and should not be called directly by the user.

            Usage:
                To stop NiceGUI, call this method on the NiceGUI application instance.

            Example:
                app = NiceGUIApp()
                app.stop()
            """
            self._state = State.STOPPING
            for t in self._shutdown_handlers:
                Client.auto_index_client.safe_invoke(t)
            self._state = State.STOPPED

    def on_connect(self, handler: Union[Callable, Awaitable]) -> None:
            """
            Called every time a new client connects to NiceGUI.

            This method allows you to register a callback function or coroutine that will be executed
            whenever a new client connects to the NiceGUI server.

            Parameters:
                handler (Union[Callable, Awaitable]): The callback function or coroutine to be executed
                    when a new client connects. The callback function can have an optional parameter of
                    `nicegui.Client`, which represents the connected client.

            Returns:
                None

            Note:
                The `on_connect` method allows you to register multiple handlers. When a new client connects,
                all registered handlers will be called in the order they were added.
            """
            self._connect_handlers.append(handler)

    def on_disconnect(self, handler: Union[Callable, Awaitable]) -> None:
            """
            Register a callback function to be called every time a new client disconnects from NiceGUI.

            Args:
                handler (Union[Callable, Awaitable]): The callback function to be registered. It can be a regular
                    function or an awaitable coroutine function.

            Returns:
                None

            Raises:
                None

            The `on_disconnect` method allows you to register a callback function that will be called every time a new
            client disconnects from NiceGUI. The callback function will receive an optional parameter of type `nicegui.Client`,
            which represents the disconnected client.

            The `handler` parameter should be a function that takes a single parameter of type `nicegui.Client` or an
            awaitable coroutine function that takes a single parameter of type `nicegui.Client`. The function will be
            called with the disconnected client as the argument.

            Example usage:
            ```python
            def my_disconnect_handler(client: nicegui.Client):
                print(f"Client {client.id} disconnected")

            app.on_disconnect(my_disconnect_handler)
            ```

            Note:
            - Multiple callback functions can be registered using the `on_disconnect` method. They will be called in the
              order they were registered.
            - The callback functions should not block or perform long-running operations, as they will block the execution
              of other NiceGUI events.
            """
            self._disconnect_handlers.append(handler)

    def on_startup(self, handler: Union[Callable, Awaitable]) -> None:
            """
            Called when NiceGUI is started or restarted.

            This method allows registering a handler function or coroutine that will be called when NiceGUI is started or restarted.
            It should be called before `ui.run()`.

            Parameters:
                handler (Union[Callable, Awaitable]): The handler function or coroutine to be registered.

            Raises:
                RuntimeError: If another startup handler is already registered.

            Example:
                def my_startup_handler():
                    # Perform startup tasks here
                    pass

                app.on_startup(my_startup_handler)

            Note:
                The registered handler will be called in the order they were registered.

            See Also:
                - `ui.run()`: The method that starts the NiceGUI event loop.

            """
            if self.is_started:
                raise RuntimeError('Unable to register another startup handler. NiceGUI has already been started.')
            self._startup_handlers.append(handler)

    def on_shutdown(self, handler: Union[Callable, Awaitable]) -> None:
            """
            Register a handler function to be called when NiceGUI is shut down or restarted.

            This method allows you to register a handler function that will be called when NiceGUI is shut down or restarted.
            The handler function will be executed before NiceGUI terminates and can be used to perform any necessary cleanup
            or finalization tasks.

            Parameters:
                handler (Union[Callable, Awaitable]): The handler function to be called on shutdown or restart.

            Returns:
                None

            Raises:
                None

            Example:
                def cleanup():
                    # Perform cleanup tasks here
                    pass

                app.on_shutdown(cleanup)

            Notes:
                - When NiceGUI is shut down or restarted, all tasks still in execution will be automatically canceled.
                - Multiple handler functions can be registered using this method. They will be called in the order they were registered.
            """
            self._shutdown_handlers.append(handler)

    def on_exception(self, handler: Callable) -> None:
        """
        Register a callback function to handle exceptions that occur within the application.

        :param handler: A callable object that takes an optional `Exception` parameter.
                        This callback function will be invoked when an exception occurs.
        :return: None

        This method allows you to register a callback function that will be called whenever an exception occurs
        within the application. The callback function should take an optional `Exception` parameter, which will
        receive the exception object that was raised.

        Example usage:

        ```python
        def handle_exception(exception: Exception) -> None:
            # Handle the exception here
            print(f"An exception occurred: {exception}")

        app.on_exception(handle_exception)
        ```

        Note that multiple callback functions can be registered, and they will be called in the order they were added.

        For more information, see the Python documentation on exception handling:
        [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
        """
        self._exception_handlers.append(handler)

    def handle_exception(self, exception: Exception) -> None:
            """
            Handle an exception by invoking all registered exception handlers.

            This method iterates over all registered exception handlers and invokes them
            to handle the given exception. If a handler is a coroutine function, it is
            scheduled as a background task using the `background_tasks.create` function.

            Parameters:
                exception (Exception): The exception to be handled.

            Returns:
                None

            Example:
                >>> app = App()
                >>> app.handle_exception(ValueError("Invalid input"))
            """
            for handler in self._exception_handlers:
                result = handler() if not inspect.signature(handler).parameters else handler(exception)
                if helpers.is_coroutine_function(handler):
                    background_tasks.create(result)

    def shutdown(self) -> None:
            """
            Shut down NiceGUI.

            This method is used to programmatically stop the NiceGUI server.
            It can only be called when auto-reload is disabled.

            Raises:
                RuntimeError: If the `auto-reload` feature is enabled, calling `shutdown()` is not supported.

            Usage:
                To shut down NiceGUI, call the `shutdown()` method on the NiceGUI instance.

            Example:
                ```
                nicegui_instance = NiceGUI()
                nicegui_instance.shutdown()
                ```

            Notes:
                - When `auto-reload` is disabled, this method will destroy the main window if it exists, or set the `should_exit` flag of the NiceGUI server instance to `True`.
                - If `auto-reload` is enabled, calling `shutdown()` will raise a `RuntimeError`.
            """
            if self.config.reload:
                raise RuntimeError('calling shutdown() is not supported when auto-reload is enabled')
            if self.native.main_window:
                self.native.main_window.destroy()
            else:
                Server.instance.should_exit = True

    def add_static_files(self,
                             url_path: str,
                             local_directory: Union[str, Path],
                             *,
                             follow_symlink: bool = False) -> None:
            """
            Add a directory of static files.

            `add_static_files()` makes a local directory available at the specified endpoint, e.g. `'/static'`.
            This is useful for providing local data like images to the frontend.
            Otherwise the browser would not be able to access the files.
            Do only put non-security-critical files in there, as they are accessible to everyone.

            To make a single file accessible, you can use `add_static_file()`.
            For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.

            Parameters:
            - url_path (str): The URL path at which the files should be served. It should start with a slash "/".
            - local_directory (Union[str, Path]): The local folder containing the files to be served as static content.
            - follow_symlink (bool, optional): Whether to follow symlinks. Defaults to False.

            Raises:
            - ValueError: If the `url_path` is set to '/' because it would hide NiceGUI's internal '/_nicegui' route.

            Example:
            ```
            app.add_static_files('/static', '/path/to/static/files')
            ```

            Note:
            - The `local_directory` should contain the static files that you want to serve.
            - If you want to serve a single file, use `add_static_file()` instead.
            - If you want to serve media files that should be streamed, use `add_media_files()` or `add_media_file()` instead.
            """
            if url_path == '/':
                raise ValueError('''Path cannot be "/", because it would hide NiceGUI's internal "/_nicegui" route.''')
            self.mount(url_path, StaticFiles(directory=str(local_directory), follow_symlink=follow_symlink))

    def add_static_file(self, *,
                            local_file: Union[str, Path],
                            url_path: Optional[str] = None,
                            single_use: bool = False,
                            ) -> str:
            """Add a single static file.

            This method allows a local file to be accessed online with enabled caching.
            If `url_path` is not specified, a path will be generated automatically.

            Args:
                local_file (Union[str, Path]): The local file to serve as static content.
                url_path (Optional[str], optional): A string that starts with a slash "/" and identifies the path at which the file should be served. Defaults to None, which generates an auto-generated URL path.
                single_use (bool, optional): Whether to remove the route after the file has been downloaded once. Defaults to False.

            Returns:
                str: The URL path which can be used to access the file.

            Raises:
                ValueError: If the specified file is not found.

            Example:
                To add a static file and get the URL path:

                ```python
                app = App()
                file_path = "/path/to/file.txt"
                url_path = app.add_static_file(local_file=file_path)
                print(url_path)
                ```

            Note:
                - To make a whole folder of files accessible, use `add_static_files()` instead.
                - For media files which should be streamed, you can use `add_media_files()` or `add_media_file()` instead.
            """
            file = Path(local_file).resolve()
            if not file.is_file():
                raise ValueError(f'File not found: {file}')
            path = f'/_nicegui/auto/static/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

            @self.get(path)
            def read_item() -> FileResponse:
                if single_use:
                    self.remove_route(path)
                return FileResponse(file, headers={'Cache-Control': 'public, max-age=3600'})

            return path

    def add_media_files(self, url_path: str, local_directory: Union[str, Path]) -> None:
            """
            Add a directory of media files to be served.

            This method allows a local directory of media files to be streamed from a specified endpoint, such as '/media'.
            Streaming media files is necessary to support proper loading and seeking of the files in a web browser.
            Without streaming, the browser would not be able to access and load the files incrementally or jump to different positions in the stream.

            It is important to note that the files added using this method are accessible to everyone, so only non-security-critical files should be placed in the directory.

            To make a single file accessible via streaming, you can use the `add_media_file()` method.
            For small static files, you can use `add_static_files()` or `add_static_file()` instead.

            Args:
                url_path (str): The URL path at which the files should be served. It should start with a slash ("/").
                local_directory (Union[str, Path]): The local directory containing the media files to be served.

            Raises:
                HTTPException: If the requested file is not found in the local directory.

            Returns:
                None
            """
            @self.get(url_path + '/{filename:path}')
            def read_item(request: Request, filename: str, nicegui_cunk_size: int = 8192) -> Response:
                filepath = Path(local_directory) / filename
                if not filepath.is_file():
                    raise HTTPException(status_code=404, detail='Not Found')
                return get_range_response(filepath, request, chunk_size=nicegui_cunk_size)

    def add_media_file(self, *,
                           local_file: Union[str, Path],
                           url_path: Optional[str] = None,
                           single_use: bool = False,
                           ) -> str:
            """Add a single media file.

            This method allows you to add a single media file to the application for streaming.
            The media file can be accessed through a URL path.

            Args:
                local_file (Union[str, Path]): The local file to serve as media content.
                url_path (Optional[str], optional): The URL path at which the file should be served.
                    If not specified, a path will be automatically generated. Defaults to None.
                single_use (bool, optional): Whether to remove the route after the media file has been downloaded once.
                    Defaults to False.

            Returns:
                str: The URL path which can be used to access the file.

            Raises:
                ValueError: If the local file is not found.

            Example:
                To add a media file named "video.mp4" located in the "/path/to/media" directory:

                >>> app.add_media_file(local_file="/path/to/media/video.mp4")

                This will generate a URL path that can be used to access the file.

            Note:
                - For streaming a whole folder of media files, use the `add_media_files()` method instead.
                - For serving small static files, you can use `add_static_files()` or `add_static_file()` methods.

            """
            file = Path(local_file).resolve()
            if not file.is_file():
                raise ValueError(f'File not found: {local_file}')
            path = f'/_nicegui/auto/media/{helpers.hash_file_path(file)}/{file.name}' if url_path is None else url_path

            @self.get(path)
            def read_item(request: Request, nicegui_cunk_size: int = 8192) -> Response:
                if single_use:
                    self.remove_route(path)
                return get_range_response(file, request, chunk_size=nicegui_cunk_size)

            return path

    def remove_route(self, path: str) -> None:
            """
            Remove routes with the given path.

            This method removes all routes from the `routes` list that have a matching `path` attribute.
            
            Parameters:
                path (str): The path to be removed from the routes.

            Returns:
                None

            Example:
                app = App()
                app.add_route('/home', home_handler)
                app.add_route('/about', about_handler)
                app.remove_route('/home')
                # Now the `routes` list only contains the '/about' route.
            """
            self.routes[:] = [r for r in self.routes if getattr(r, 'path', None) != path]

    def reset(self) -> None:
            """
            Reset the app to its initial state.

            This method clears the app's storage and resets all event handlers to their initial state.
            It is useful for testing purposes or when you want to restore the app to its original state.

            Usage:
                app.reset()

            Returns:
                None
            """
            self.storage.clear()
            self._startup_handlers.clear()
            self._shutdown_handlers.clear()
            self._connect_handlers.clear()
            self._disconnect_handlers.clear()
            self._exception_handlers[:] = [log.exception]
