from typing import Any, Callable, Optional

from nicegui.elements.mixins.disableable_element import DisableableElement
from nicegui.elements.mixins.value_element import ValueElement


class Pagination(ValueElement, DisableableElement):

    def __init__(self,
                 min: int, max: int, *,  # pylint: disable=redefined-builtin
                 direction_links: bool = False,
                 value: Optional[int] = ...,  # type: ignore
                 on_change: Optional[Callable[..., Any]] = None) -> None:
        """Pagination

        A pagination element wrapping Quasar's `QPagination <https://quasar.dev/vue-components/pagination>`_ component.

        :param min: minimum page number
        :param max: maximum page number
        :param direction_links: whether to show first/last page links
        :param value: initial page (defaults to `min` if no value is provided)
        :param on_change: callback to be invoked when the value changes
        """
        super().__init__(tag='q-pagination', value=value, on_value_change=on_change)
        self._props['min'] = min
        self._props['max'] = max
        self._props['direction-links'] = direction_links
        if value is ...:
            self.value = min
