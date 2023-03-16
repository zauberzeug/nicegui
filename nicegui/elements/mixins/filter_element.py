from typing import Any, Callable, Optional

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class FilterElement(Element):
    FILTER_PROP = 'filter'
    filter = BindableProperty(on_change=lambda sender, filter: sender.on_filter_change(filter))

    def __init__(self, *, filter: Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.filter = filter
        self._props[self.FILTER_PROP] = filter

    def bind_filter_to(self, target_object: Any, target_name: str = 'filter', forward: Callable = lambda x: x):
        bind_to(self, 'filter', target_object, target_name, forward)
        return self

    def bind_filter_from(self, target_object: Any, target_name: str = 'filter', backward: Callable = lambda x: x):
        bind_from(self, 'filter', target_object, target_name, backward)
        return self

    def bind_filter(self, target_object: Any, target_name: str = 'filter', *,
                    forward: Callable = lambda x: x, backward: Callable = lambda x: x):
        bind(self, 'filter', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_filter(self, filter: str) -> None:
        self.filter = filter

    def on_filter_change(self, filter: str) -> None:
        self._props[self.FILTER_PROP] = filter
        self.update()
