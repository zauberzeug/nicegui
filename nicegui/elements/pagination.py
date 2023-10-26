from typing import Any, Callable, Optional

from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement


class Pagination(ValueElement, DisableableElement):

    """Pagination

        A pagination element wrapping Quasar's
        `QPagination <https://quasar.dev/vue-components/pagination>`_ component.

        :param min: minimum (start) value in the pagination element (e.g. 1)
        :param max: miximum (end) value in the pagination element (e.g. 2, 10)
        :param value: initial or current selection (defaults to min if no value provided)
        :param on_change: callback to be invoked when the value changes
    """

    def __init__(self, min: int, max: int, *, direction_links: bool = False,
                 value: Optional[int] = ..., on_change: Optional[Callable[..., Any]] = None) -> None:
        super().__init__(tag='q-pagination', value=value, on_value_change=on_change)
        self._props['min'] = min
        self._props['max'] = max
        self._props['direction-links'] = direction_links
        if value is ...:
            self.value = min