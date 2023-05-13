import inspect
import types
from dataclasses import dataclass, field
from multiprocessing import Queue
from typing import Any, Dict, Optional

import webview

from .helpers import KWONLY_SLOTS

queue = Queue()


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
            queue.put((name, args[1:], kwargs))  # NOTE args[1:] to skip self
        return wrapper

    for name, attr in inspect.getmembers(cls):
        if name.startswith('__'):
            continue

        if inspect.isfunction(attr) or inspect.ismethod(attr):
            setattr(Proxy, name, mock_method(name))

    return Proxy


@dataclass(**KWONLY_SLOTS)
class Native:

    start_args: Dict[str, Any] = field(default_factory=dict)
    window_args: Dict[str, Any] = field(default_factory=dict)
    window: webview.Window = create_proxy(webview.Window)()
