import asyncio
import inspect
import logging
import warnings
from dataclasses import dataclass, field
from functools import partial
from multiprocessing import Queue
from typing import Any, Callable, Dict, Optional, Tuple

from .helpers import KWONLY_SLOTS

method_queue: Queue = Queue()
response_queue: Queue = Queue()

try:
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
        from webview.window import FixPoint

    class WindowProxy(webview.Window):

        def __init__(self) -> None:
            pass  # NOTE we don't call super().__init__ here because this is just a proxy to the actual window

        async def get_always_on_top(self) -> bool:
            """Get whether the window is always on top."""
            return await self._request()

        def set_always_on_top(self, on_top: bool) -> None:
            """Set whether the window is always on top."""
            self._send(on_top)

        async def get_size(self) -> Tuple[int, int]:
            """Get the window size as tuple (width, height)."""
            return await self._request()

        async def get_position(self) -> Tuple[int, int]:
            """Get the window position as tuple (x, y)."""
            return await self._request()

        def load_url(self, url: str) -> None:
            self._send(url)

        def load_html(self, content: str, base_uri: str = ...) -> None:
            self._send(content, base_uri)

        def load_css(self, stylesheet: str) -> None:
            self._send(stylesheet)

        def set_title(self, title: str) -> None:
            self._send(title)

        async def get_cookies(self) -> Any:
            return await self._request()

        async def get_current_url(self) -> str:
            return await self._request()

        def destroy(self) -> None:
            self._send()

        def show(self) -> None:
            self._send()

        def hide(self) -> None:
            self._send()

        def set_window_size(self, width: int, height: int) -> None:
            self._send(width, height)

        def resize(self, width: int, height: int, fix_point: FixPoint = FixPoint.NORTH | FixPoint.WEST) -> None:
            self._send(width, height, fix_point)

        def minimize(self) -> None:
            self._send()

        def restore(self) -> None:
            self._send()

        def toggle_fullscreen(self) -> None:
            self._send()

        def move(self, x: int, y: int) -> None:
            self._send(x, y)

        async def evaluate_js(self, script: str) -> str:
            return await self._request(script)

        async def create_confirmation_dialog(self, title: str, message: str) -> bool:
            return await self._request(title, message)

        async def create_file_dialog(
            self,
            dialog_type: int = webview.OPEN_DIALOG,
            directory: str = '',
            allow_multiple: bool = False,
            save_filename: str = '',
            file_types: Tuple[str, ...] = (),
        ) -> Tuple[str, ...]:
            return await self._request(
                dialog_type=dialog_type,
                directory=directory,
                allow_multiple=allow_multiple,
                save_filename=save_filename,
                file_types=file_types,
            )

        def expose(self, function: Callable) -> None:
            raise NotImplementedError(f'exposing "{function}" is not supported')

        def _send(self, *args: Any, **kwargs: Any) -> None:
            name = inspect.currentframe().f_back.f_code.co_name
            method_queue.put((name, args, kwargs))

        async def _request(self, *args: Any, **kwargs: Any) -> Any:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    method_queue.put((name, args, kwargs))
                    return response_queue.get()  # wait for the method to be called and writing its result to the queue
                except Exception:
                    logging.exception(f'error in {name}')
            name = inspect.currentframe().f_back.f_code.co_name
            return await asyncio.get_event_loop().run_in_executor(None, partial(wrapper, *args, **kwargs))

        def signal_server_shutdown(self) -> None:
            self._send()

except ModuleNotFoundError:
    class WindowProxy():
        pass  # just a dummy if webview is not installed


@dataclass(**KWONLY_SLOTS)
class Native:
    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
    main_window: Optional[WindowProxy] = None
