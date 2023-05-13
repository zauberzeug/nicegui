import asyncio
import inspect
import logging
from dataclasses import dataclass, field
from functools import partial
from multiprocessing import Queue
from typing import Any, Dict, get_type_hints

import webview

from . import background_tasks
from .helpers import KWONLY_SLOTS

method_queue = Queue()
response_queue = Queue()


def create_proxy(cls):
    class Proxy:
        def __getattr__(self, name):
            if name.startswith('__'):
                return super().__getattr__(name)
            print(f'get {name}: properties are not yet supported')

        def __setattr__(self, name, value):
            if name.startswith('__'):
                super().__setattr__(name, value)
                return
            print(f'set {name}: properties are not yet supported')

    def mock_method(name):
        def wrapper(*args, **kwargs):
            method_queue.put((name, args[1:], kwargs))  # NOTE args[1:] to skip self
        return wrapper

    def mock_coroutine(name):
        def wrapper(*args, **kwargs):
            try:
                method_queue.put((name, args[1:], kwargs))  # NOTE args[1:] to skip self
                result = response_queue.get()  # wait for the method to be called and write its result to the queue
                ic(result)
                logging.info(f'got result: {result}')
                return result
            except Exception:
                logging.exception(f'error in {name}')

        async def awaitable_wrapper(_, *args, **kwargs):
            return await asyncio.get_event_loop().run_in_executor(None, partial(wrapper, *args, **kwargs))

        return awaitable_wrapper

    def has_return_value(name):
        if get_type_hints(attr).get('return', None) is not None:
            return True
        if name == 'create_file_dialog':
            return True
        return False

    for name, attr in inspect.getmembers(cls):
        if name.startswith('__'):
            continue

        if inspect.isfunction(attr) or inspect.ismethod(attr):
            mock = mock_coroutine(name) if has_return_value(name) else mock_method(name)
            setattr(Proxy, name, mock)
        else:
            print(f'skip {name}: only methods are supported', flush=True)

    return Proxy


@ dataclass(**KWONLY_SLOTS)
class Native:

    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
    window: webview.Window = create_proxy(webview.Window)()
