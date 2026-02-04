# pylint: disable=C0116
from __future__ import annotations

import inspect
import warnings
from collections.abc import Callable
from multiprocessing import Queue
from typing import Any

from .. import run
from ..logging import log

method_queue: Queue | None = None
response_queue: Queue | None = None


def create_queues() -> None:
    """Create the message queues. (For internal use only.)"""
    global method_queue, response_queue  # pylint: disable=global-statement # noqa: PLW0603
    method_queue = Queue()
    response_queue = Queue()


def remove_queues() -> None:
    """Remove the message queues by closing them and waiting for threads to finish. (For internal use only.)"""
    global method_queue, response_queue  # pylint: disable=global-statement # noqa: PLW0603
    if method_queue is not None:
        method_queue.close()
        method_queue.join_thread()
        method_queue = None
    if response_queue is not None:
        response_queue.close()
        response_queue.join_thread()
        response_queue = None


try:
    with warnings.catch_warnings():
        # webview depends on bottle which uses the deprecated CGI function (https://github.com/bottlepy/bottle/issues/1403)
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        import webview
        from webview.window import FixPoint

    class WindowProxy(webview.Window):

        def __init__(self) -> None:  # pylint: disable=super-init-not-called
            pass  # NOTE we don't call super().__init__ here because this is just a proxy to the actual window

        async def get_always_on_top(self) -> bool:
            """Get whether the window is always on top."""
            return await self._request()

        def set_always_on_top(self, on_top: bool) -> None:
            """Set whether the window is always on top."""
            self._send(on_top)

        async def get_size(self) -> tuple[int, int]:
            """Get the window size as tuple (width, height)."""
            return await self._request()

        async def get_position(self) -> tuple[int, int]:
            """Get the window position as tuple (x, y)."""
            return await self._request()

        def load_url(self, url: str) -> None:
            self._send(url)

        def load_html(self, html: str, base_uri: str = ...) -> None:  # type: ignore
            self._send(html, base_uri)

        def load_css(self, stylesheet: str) -> None:
            self._send(stylesheet)

        def set_title(self, title: str) -> None:
            self._send(title)

        async def get_cookies(self) -> Any:  # pylint: disable=invalid-overridden-method
            return await self._request()

        async def get_current_url(self) -> str:  # type: ignore # pylint: disable=invalid-overridden-method
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

        def maximize(self) -> None:
            self._send()

        def minimize(self) -> None:
            self._send()

        def restore(self) -> None:
            self._send()

        def toggle_fullscreen(self) -> None:
            self._send()

        def move(self, x: int, y: int) -> None:
            self._send(x, y)

        async def evaluate_js(  # type: ignore # pylint: disable=arguments-differ,invalid-overridden-method
            self,
            script: str,
        ) -> str:
            return await self._request(script)

        async def create_confirmation_dialog(  # type: ignore # pylint: disable=invalid-overridden-method
            self,
            title: str,
            message: str,
        ) -> bool:
            return await self._request(title, message)

        async def create_file_dialog(  # type: ignore # pylint: disable=invalid-overridden-method
            self,
            dialog_type: int = webview.FileDialog.OPEN if hasattr(webview, 'FileDialog') else webview.OPEN_DIALOG,
            directory: str = '',
            allow_multiple: bool = False,
            save_filename: str = '',
            file_types: tuple[str, ...] = (),
        ) -> tuple[str, ...] | None:
            return await self._request(
                dialog_type=dialog_type,
                directory=directory,
                allow_multiple=allow_multiple,
                save_filename=save_filename,
                file_types=file_types,
            )

        def expose(self, function: Callable) -> None:  # type: ignore # pylint: disable=arguments-differ
            raise NotImplementedError(f'exposing "{function}" is not supported')

        def _send(self, *args: Any, **kwargs: Any) -> None:
            assert method_queue is not None
            name = inspect.currentframe().f_back.f_code.co_name  # type: ignore
            method_queue.put((name, args, kwargs))

        async def _request(self, *args: Any, **kwargs: Any) -> Any:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                assert method_queue is not None
                assert response_queue is not None
                try:
                    method_queue.put((name, args, kwargs))
                    return response_queue.get()  # wait for the method to be called and writing its result to the queue
                except Exception:
                    log.exception(f'error in {name}')
                    return None
            name = inspect.currentframe().f_back.f_code.co_name  # type: ignore
            return await run.io_bound(wrapper, *args, **kwargs)

        def signal_server_shutdown(self) -> None:
            """Signal the server shutdown."""
            self._send()

except ModuleNotFoundError:
    class WindowProxy:  # type: ignore
        pass  # just a dummy if webview is not installed
