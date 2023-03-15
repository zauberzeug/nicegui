from typing import Any, Callable, Optional

from ...binding import BindableProperty, bind, bind_from, bind_to
from ...element import Element


class FilterElement(Element):
    FILTER_PROP = 'filter'
    filter = BindableProperty(on_change=lambda sender, filter_by: sender.on_filter_change(filter_by))

    def __init__(self, *, filter_by: Optional[str] = '', **kwargs) -> None:
        super().__init__(**kwargs)
        self.filter = filter_by
        self._props[self.FILTER_PROP] = filter_by

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

    def set_filter(self, filter_by: str) -> None:
        self.filter = filter_by

    def on_filter_change(self, filter_by: str) -> None:
        self._props[self.FILTER_PROP] = filter_by
        self.update()
