import asyncio
import inspect
import logging
from dataclasses import dataclass, field
from functools import partial
from multiprocessing import Queue
from typing import Any, Dict, Tuple

import webview
from webview.window import FixPoint

from .helpers import KWONLY_SLOTS

method_queue = Queue()
response_queue = Queue()


class WindowProxy(webview.Window):
    def __init__(self):
        pass  # NOTE we don't call super().__init__ here because this is just a proxy to the actual window

    async def get_size(self) -> Tuple[int, int]:
        return await self._send_async()

    async def get_position(self) -> Tuple[int, int]:
        return await self._send_async()

    def load_url(self, url: str) -> None:
        self._send(url)

    def load_html(self, content: str, base_uri: str = ...) -> None:
        self._send(content, base_uri)

    def load_css(self, stylesheet: str) -> None:
        self._send(stylesheet)

    def set_title(self, title: str) -> None:
        self.send(title)

    async def get_cookies(self) -> None:
        return await self._send_async()

    async def get_current_url(self) -> None:
        return await self._send_async()

    def destroy(self) -> None:
        self._send()

    def show(self) -> None:
        self._send()

    def hide(self) -> None:
        self._send()

    def set_window_size(self, width: int, height: int) -> None:
        self._send(width, height)

    def resize(self, width: int, height: int, fix_point=FixPoint.NORTH | FixPoint.WEST) -> None:
        self._send(width, height, fix_point)

    def minimize(self) -> None:
        self._send()

    def restore(self) -> None:
        self._send()

    def toggle_fullscreen(self) -> None:
        self._send()

    def move(self, x: int, y: int) -> None:
        self._send(x, y)

    def evaluate_js(self, script: str) -> Any:
        return self._send(script)

    async def create_confirmation_dialog(self, title: str, message: str) -> bool:
        return await self._send_async(title, message)

    async def create_file_dialog(
        self,
        dialog_type: int = webview.OPEN_DIALOG,
        directory: str = '',
        allow_multiple: bool = False,
        save_filename: str = '',
        file_types: Tuple[str, ...] = ...
    ) -> Tuple[str, ...]:
        return await self._send_async(dialog_type, directory, allow_multiple, save_filename, file_types)

    def expose(self, function) -> None:
        raise NotImplementedError(f'exposing "{function}" is not supported')

    def _send(self, *args, **kwargs) -> Any:
        name = inspect.currentframe().f_back.f_code.co_name
        return method_queue.put((name, args, kwargs))

    async def _send_async(self, *args, **kwargs) -> Any:
        name = inspect.currentframe().f_back.f_code.co_name

        def wrapper(*args, **kwargs):
            try:
                method_queue.put((name, args[1:], kwargs))  # NOTE args[1:] to skip self
                return response_queue.get()  # wait for the method to be called and writing its result to the queue
            except Exception:
                logging.exception(f'error in {name}')

        return await asyncio.get_event_loop().run_in_executor(None, partial(wrapper, *args, **kwargs))

    def signal_server_shutdown(self) -> None:
        self._send()


@dataclass(**KWONLY_SLOTS)
class Native:
    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
    main_window: WindowProxy = WindowProxy()
