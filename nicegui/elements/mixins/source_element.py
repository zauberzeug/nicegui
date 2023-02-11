from typing import Any, Callable

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class SourceElement(Element):
    source = BindableProperty(on_change=lambda sender, source: sender.on_source_change(source))

    def __init__(self, *, source: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.source = source
        self._props['src'] = source

    def bind_source_to(self, target_object: Any, target_name: str = 'source', forward: Callable = lambda x: x):
        bind_to(self, 'source', target_object, target_name, forward)
        return self

    def bind_source_from(self, target_object: Any, target_name: str = 'source', backward: Callable = lambda x: x):
        bind_from(self, 'source', target_object, target_name, backward)
        return self

    def bind_source(self, target_object: Any, target_name: str = 'source', *,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'source', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_source(self, source: str) -> None:
        self.source = source

    def on_source_change(self, source: str) -> None:
        self._props['src'] = source
        self.update()
